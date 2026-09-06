#!/usr/bin/env python3
"""Unit 0.5 — rebuild the port kit's Data/*.csv from the Godot source
(the PORT-BRIEF: "the GDScript reads as exact pseudocode; every constant
in it is canon"). Deterministic, re-runnable; run from anywhere.

Outputs to ue/Restoration/Data/:
  Rooms.csv      name, center_x, center_z, width, depth   (Godot meters)
  Doors.csv      room_a, room_b, gap_x, gap_z, width, axis, kind
  Stations.csv   id, label, x, y, z
  Monitors.csv   cam_pos, look_at, monitor_pos, yaw_rad, label
  DemoOpen.csv   room (the DEMO whitelist)
  Timings.csv    file, constant, value  (every tuning number, with its home)
  GameText.csv   Key,SourceString (from translations/strings.csv keys)
  Landmarks.csv  name, room, x, z, kind, script  (unit C7: every top-level
                 positioned node world_builder.gd spawns — doors, stations,
                 rigs, interactables, NPCs, PropKit set pieces — recovered
                 by walking _ready() over the source with a restricted
                 GDScript evaluator; see the LANDMARKS section below)
"""
import csv
import math
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "ue", "Restoration", "Data")
os.makedirs(OUT, exist_ok=True)

wb = open(os.path.join(ROOT, "scripts", "world_builder.gd"), encoding="utf-8").read()


def block(name, opener="[", closer="]"):
    pat = r"const %s\s*:=\s*%s(.*?)\n%s" % (name, re.escape(opener), re.escape(closer))
    m = re.search(pat, wb, re.S)
    return m.group(1) if m else ""


## Rooms
rooms = re.findall(r'"([^"]+)":\s*\[([-\d.]+),\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)\]',
                   block("ROOMS", "{", "}"))
with open(os.path.join(OUT, "Rooms.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["name", "center_x", "center_z", "width", "depth"])
    for r in rooms:
        w.writerow(r)

## Doors
doors = re.findall(
    r'\["([^"]+)",\s*"([^"]+)",\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+),\s*"([xz])",\s*"([^"]*)"\]',
    block("DOORS"))
with open(os.path.join(OUT, "Doors.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["room_a", "room_b", "gap_x", "gap_z", "width", "axis", "kind"])
    for d in doors:
        w.writerow(d)

## Stations
stations = re.findall(
    r'\["([^"]+)",\s*"([^"]+)",\s*Vector3\(([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)\)\]',
    block("STATIONS"))
with open(os.path.join(OUT, "Stations.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "label", "x", "y", "z"])
    for s in stations:
        w.writerow(s)

## Monitors
monitors = re.findall(
    r'\[Vector3\(([^)]+)\),\s*Vector3\(([^)]+)\),\s*Vector3\(([^)]+)\),\s*([^,\]]+),\s*"([^"]+)"\]',
    block("MONITORS"))
with open(os.path.join(OUT, "Monitors.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["cam_pos", "look_at", "monitor_pos", "yaw_rad", "label"])
    for m in monitors:
        w.writerow([x.strip() for x in m])

## Demo whitelist (single-line const — match on its own line only)
demo = re.findall(r'"([^"]+)"',
                  re.search(r"const DEMO_OPEN\s*:=\s*\[([^\]]*)\]", wb).group(1))
with open(os.path.join(OUT, "DemoOpen.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["room"])
    for d in demo:
        w.writerow([d])

## Timings: every tuning constant across scripts, with its home
rows = []
for fn in sorted(os.listdir(os.path.join(ROOT, "scripts"))):
    if not fn.endswith(".gd"):
        continue
    for i, line in enumerate(open(os.path.join(ROOT, "scripts", fn)), 1):
        m = re.match(r"\s*const\s+([A-Z][A-Z0-9_]*)\s*:?=\s*([-\d.]+)\s*(?:#.*)?$", line)
        if m:
            rows.append([fn, m.group(1), m.group(2)])
with open(os.path.join(OUT, "Timings.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["file", "constant", "value"])
    w.writerows(rows)

## GameText: keys from the shipped translations table
keys = []
with open(os.path.join(ROOT, "translations", "strings.csv"), newline="") as f:
    rd = csv.reader(f)
    header = next(rd)
    for row in rd:
        if row and row[0].strip():
            keys.append(row[0])
with open(os.path.join(OUT, "GameText.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Key", "SourceString"])
    for k in keys:
        w.writerow([k, k])

## ---------------------------------------------------------------------------
## LANDMARKS (unit C7)
##
## world_builder.gd has no single landmark table: interactables, NPCs, rigs
## and set pieces are spawned in code, inside loops and helper functions
## (README ledger, commit "Unit 0.5"). So this section EXECUTES the spawn
## code instead of pattern-matching it: a restricted evaluator for the
## GDScript subset world_builder.gd actually uses (var/assignment, for over
## ints and literal lists, if/elif/else, return, string formatting, Vector3
## arithmetic, .new(), PropKit/CharacterKit factories, local helper calls)
## walks _ready() and records every node handed to add_child(...) on the
## builder itself, with the position it was given. Anything the evaluator
## cannot follow becomes UNKNOWN and is REPORTED, never guessed.
##
## Policies (all stated, none invented):
##   * GameState.DEMO is False: the table is the full game, not the demo
##     (world_builder.gd _spawn_bench/_spawn_rundown/... `if GameState.DEMO`).
##   * Every other GameState test (has_key, has_fire_tape, signals_known,
##     ng_relic) is unknown here and is taken as TRUE, i.e. a fresh save:
##     every conditional pickup is listed. Conditions are listed in the
##     LANDMARK-GATES report so the port can gate them the same way.
##   * Raw geometry is not a landmark: walls, floors, colliders, bare
##     MeshInstance3D/StaticBody3D, shapes, materials, and lights are
##     excluded (lights are unit C18's Lighting.csv). _build_room/_wall_run/
##     _cut/_box/_collider are skipped whole; ROOMS/DOORS already carry them.
##   * A row is a node added to the builder (add_child(x)) with a position;
##     children of a landmark (its meshes, lectern, tag, coil) are folded
##     into the parent row. Nodes without a position (managers/systems) are
##     reported as LANDMARK-POSITIONLESS, not written.
##   * MonitorRig has no .position; its screen stands at monitor_position
##     (monitor_rig.gd lines 43-57), so that is the row's x,z.
##   * PropKit.felt_run(length, self, pos, yaw) stamps onto the builder at
##     pos (prop_kit.gd line 526) and so is a row; PropKit.baseboard stamps
##     per room from ROOMS and is room geometry (excluded).
##   * A top-level Label3D (a floating tag) names the top-level node spawned
##     by the same function at the same x,z (the CAM 1..3 pedestals); one
##     with no such node is itself a marker row (CHUM'S MARK); one whose
##     text is runtime-only (the ng_relic tag) is reported and dropped.
##   * room = every ROOMS rectangle containing (x,z) within WALL_T/2 + 1cm;
##     several (a door on a shared wall) are joined with "|"; none = OPEN.
##   * name = the node's own label text (Label3D child / _dock_body tag), else
##     door_label / sign_text / label_text / slate_text, else its class; then
##     four id joins from the node's own fields: LogStation "<tag> · <station_
##     name>", KeyItem "<tag> · <key_id>", AssetPickup "<tag> · <asset_id>",
##     ReadableProp "<doc_id> · <label>". y is not a column (the box asks for
##     x,z); every listed y is floor-relative and lives in the source.
## ---------------------------------------------------------------------------

UNKNOWN = object()  # anything the evaluator cannot follow


class Vec3:
    __slots__ = ("x", "y", "z")

    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def __add__(self, o):
        return Vec3(self.x + o.x, self.y + o.y, self.z + o.z) if isinstance(o, Vec3) else UNKNOWN

    def __sub__(self, o):
        return Vec3(self.x - o.x, self.y - o.y, self.z - o.z) if isinstance(o, Vec3) else UNKNOWN

    def __mul__(self, o):
        return Vec3(self.x * o, self.y * o, self.z * o) if isinstance(o, (int, float)) else UNKNOWN


class GNode:
    """A spawned node: what class made it, where it was put, what it was called."""

    def __init__(self, kind, func):
        self.kind = kind
        self.func = func
        self.attrs = {}
        self.pos = None
        self.tag = None
        self.parent = None
        self.top = False


class ReturnSignal(Exception):
    pass


## --- tokenizer / parser for the expression subset -------------------------
_TOKEN = re.compile(r"""
    (?P<num>\d+\.\d*|\.\d+|\d+)
  | (?P<str>"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')
  | (?P<id>[A-Za-z_]\w*)
  | (?P<op>:=|==|!=|<=|>=|->|[-+*/%()\[\]{},.:=<>])
  | (?P<ws>\s+)
""", re.X)


def tokenize(s):
    out, i = [], 0
    while i < len(s):
        m = _TOKEN.match(s, i)
        if not m:
            raise SyntaxError("bad token at %r" % s[i:i + 20])
        i = m.end()
        if m.lastgroup == "ws":
            continue
        out.append((m.lastgroup, m.group()))
    out.append(("eof", ""))
    return out


class Parser:
    KEYWORDS = {"and", "or", "not", "in", "if", "else", "as", "true", "false", "null", "self"}

    def __init__(self, s):
        self.toks = tokenize(s)
        self.i = 0

    def peek(self, k=0):
        return self.toks[self.i + k]

    def take(self, val=None):
        t = self.toks[self.i]
        if val is not None and t[1] != val:
            raise SyntaxError("expected %r got %r" % (val, t[1]))
        self.i += 1
        return t

    def at(self, val):
        return self.toks[self.i][1] == val and self.toks[self.i][0] != "str"

    def parse(self):
        e = self.ternary()
        if self.peek()[0] != "eof":
            raise SyntaxError("trailing %r" % self.peek()[1])
        return e

    def ternary(self):
        e = self.or_()
        if self.at("if"):
            self.take()
            c = self.or_()
            self.take("else")
            other = self.ternary()
            return ("tern", c, e, other)
        return e

    def or_(self):
        e = self.and_()
        while self.at("or"):
            self.take()
            e = ("or", e, self.and_())
        return e

    def and_(self):
        e = self.not_()
        while self.at("and"):
            self.take()
            e = ("and", e, self.not_())
        return e

    def not_(self):
        if self.at("not"):
            self.take()
            return ("not", self.not_())
        return self.cmp()

    def cmp(self):
        e = self.add()
        while self.peek()[1] in ("==", "!=", "<", ">", "<=", ">=", "in") and self.peek()[0] != "str":
            op = self.take()[1]
            e = ("bin", op, e, self.add())
        return e

    def add(self):
        e = self.mul()
        while self.peek()[1] in ("+", "-") and self.peek()[0] == "op":
            op = self.take()[1]
            e = ("bin", op, e, self.mul())
        return e

    def mul(self):
        e = self.unary()
        while self.peek()[1] in ("*", "/", "%") and self.peek()[0] == "op":
            op = self.take()[1]
            e = ("bin", op, e, self.unary())
        return e

    def unary(self):
        if self.peek() == ("op", "-"):
            self.take()
            return ("neg", self.unary())
        return self.postfix()

    def postfix(self):
        e = self.primary()
        while True:
            t = self.peek()
            if t == ("op", "."):
                self.take()
                name = self.take()[1]
                if self.at("("):
                    e = ("mcall", e, name, self.args())
                else:
                    e = ("attr", e, name)
            elif t == ("op", "["):
                self.take()
                idx = self.ternary()
                self.take("]")
                e = ("index", e, idx)
            elif t == ("op", "("):
                e = ("call", e, self.args())
            elif t == ("id", "as"):
                self.take()
                self.take()  # the type name
            else:
                return e

    def args(self):
        self.take("(")
        out = []
        while not self.at(")"):
            out.append(self.ternary())
            if self.at(","):
                self.take()
        self.take(")")
        return out

    def primary(self):
        kind, val = self.peek()
        if kind == "num":
            self.take()
            return ("num", float(val) if "." in val else int(val))
        if kind == "str":
            self.take()
            return ("str", bytes(val[1:-1], "utf-8").decode("unicode_escape").encode("latin-1").decode("utf-8"))
        if kind == "id":
            self.take()
            if val == "true":
                return ("const", True)
            if val == "false":
                return ("const", False)
            if val == "null":
                return ("const", None)
            return ("name", val)
        if val == "(":
            self.take()
            e = self.ternary()
            self.take(")")
            return e
        if val == "[":
            self.take()
            items = []
            while not self.at("]"):
                items.append(self.ternary())
                if self.at(","):
                    self.take()
            self.take("]")
            return ("list", items)
        if val == "{":
            self.take()
            items = []
            while not self.at("}"):
                k = self.ternary()
                self.take(":")
                items.append((k, self.ternary()))
                if self.at(","):
                    self.take()
            self.take("}")
            return ("dict", items)
        raise SyntaxError("unexpected %r" % val)


## --- the evaluator ---------------------------------------------------------
class Builder:
    GEOMETRY_FUNCS = {"_build_room", "_wall_run", "_cut", "_box", "_collider"}
    EXCLUDED_KIND = re.compile(r"(Mesh|Shape3D|Material|Material3D|Texture2D)$")
    EXCLUDED_KINDS = {"MeshInstance3D", "StaticBody3D", "CollisionShape3D", "OmniLight3D",
                      "DirectionalLight3D", "WorldEnvironment"}

    def __init__(self, source, propkit_sigs, charkit_names):
        self.propkit_sigs = propkit_sigs      # name -> (return type, param names)
        self.charkit_names = charkit_names
        self.globals = {"PI": math.pi, "TAU": math.tau}
        self.funcs = {}                       # name -> (params, body)
        self.top = []                         # nodes handed to the builder's add_child
        self.children = []                    # nodes handed to another node's add_child
        self.unparsed = []                    # statements the evaluator could not follow
        self.gates = []                       # (func, condition text) for unknown ifs
        self.func_stack = []
        self._load(source)

    ## -- source → logical lines → blocks
    @staticmethod
    def _strip_comment(line):
        out, q, i = [], None, 0
        while i < len(line):
            c = line[i]
            if q:
                out.append(c)
                if c == "\\" and i + 1 < len(line):
                    out.append(line[i + 1])
                    i += 1
                elif c == q:
                    q = None
            elif c in "\"'":
                q = c
                out.append(c)
            elif c == "#":
                break
            else:
                out.append(c)
            i += 1
        return "".join(out).rstrip()

    @staticmethod
    def _depth(s):
        d, q, i = 0, None, 0
        while i < len(s):
            c = s[i]
            if q:
                if c == "\\":
                    i += 1
                elif c == q:
                    q = None
            elif c in "\"'":
                q = c
            elif c in "([{":
                d += 1
            elif c in ")]}":
                d -= 1
            i += 1
        return d

    def _load(self, source):
        logical = []  # (indent, text)
        buf, depth, indent = [], 0, 0
        for raw in source.split("\n"):
            line = self._strip_comment(raw)
            if not line.strip() and not buf:
                continue
            if not buf:
                indent = len(line) - len(line.lstrip("\t"))
            buf.append(line.strip())
            depth += self._depth(line)
            if depth <= 0:
                logical.append((indent, " ".join(buf)))
                buf, depth = [], 0
        # blocks by indentation
        def build(i, ind):
            items = []
            while i < len(logical) and logical[i][0] >= ind:
                if logical[i][0] > ind:
                    raise SyntaxError("dedent error near %r" % logical[i][1])
                text = logical[i][1]
                i += 1
                kids = []
                if text.endswith(":"):
                    kids, i = build(i, ind + 1) if i < len(logical) and logical[i][0] > ind else ([], i)
                items.append((text, kids))
            return items, i
        tree, _ = build(0, 0)
        for text, kids in tree:
            m = re.match(r"func\s+(\w+)\s*\((.*?)\)", text)
            if m:
                params = [p.split(":")[0].strip() for p in m.group(2).split(",") if p.strip()]
                self.funcs[m.group(1)] = (params, kids)
                continue
            m = re.match(r"(?:const|var)\s+(\w+)\s*(?::\s*\w+)?\s*(?::=|=)\s*(.*)$", text)
            if m:
                self.globals[m.group(1)] = self.eval_text(m.group(2), {})
                continue
            m = re.match(r"var\s+(\w+)\s*:", text)
            if m:
                self.globals[m.group(1)] = UNKNOWN

    ## -- expressions
    def eval_text(self, text, env):
        try:
            ast = Parser(text).parse()
        except SyntaxError:
            self.unparsed.append((self.func_stack[-1] if self.func_stack else "<top>", text))
            return UNKNOWN
        return self.ev(ast, env)

    def lookup(self, name, env):
        if name in env:
            return env[name]
        if name in self.globals:
            return self.globals[name]
        return UNKNOWN

    def ev(self, a, env):
        t = a[0]
        if t in ("num", "str", "const"):
            return a[1]
        if t == "name":
            return self.lookup(a[1], env)
        if t == "list":
            return [self.ev(x, env) for x in a[1]]
        if t == "dict":
            return {self.ev(k, env): self.ev(v, env) for k, v in a[1]}
        if t == "neg":
            v = self.ev(a[1], env)
            return -v if isinstance(v, (int, float)) else UNKNOWN
        if t == "not":
            v = self.ev(a[1], env)
            return (not v) if isinstance(v, bool) else UNKNOWN
        if t == "tern":
            c = self.ev(a[1], env)
            return self.ev(a[2], env) if self.truth(c) else self.ev(a[3], env)
        if t == "and":
            l = self.ev(a[1], env)
            if l is False:
                return False
            r = self.ev(a[2], env)
            return (l and r) if isinstance(l, bool) and isinstance(r, bool) else UNKNOWN
        if t == "or":
            l = self.ev(a[1], env)
            if l is True:
                return True
            r = self.ev(a[2], env)
            return (l or r) if isinstance(l, bool) and isinstance(r, bool) else UNKNOWN
        if t == "bin":
            return self.binop(a[1], self.ev(a[2], env), self.ev(a[3], env))
        if t == "attr":
            obj = self.ev(a[1], env)
            if a[1] == ("name", "GameState") and a[2] == "DEMO":
                return False                           # policy: the full game
            if isinstance(obj, Vec3):
                return getattr(obj, a[2], UNKNOWN)
            if isinstance(obj, GNode):
                return obj.attrs.get(a[2], UNKNOWN)
            return UNKNOWN
        if t == "index":
            obj, idx = self.ev(a[1], env), self.ev(a[2], env)
            if isinstance(obj, GNode):
                return obj                              # dict-returning factory: same piece
            if isinstance(obj, list) and isinstance(idx, int) and 0 <= idx < len(obj):
                return obj[idx]
            if isinstance(obj, dict) and idx in obj:
                return obj[idx]
            return UNKNOWN
        if t == "call":
            return self.call(a[1], [self.ev(x, env) for x in a[2]], env)
        if t == "mcall":
            return self.mcall(a[1], a[2], [self.ev(x, env) for x in a[3]], env)
        raise AssertionError(t)

    @staticmethod
    def truth(v):
        return True if v is UNKNOWN else bool(v)

    @staticmethod
    def binop(op, l, r):
        if l is UNKNOWN or r is UNKNOWN:
            return UNKNOWN
        num = isinstance(l, (int, float)) and isinstance(r, (int, float))
        if op == "+":
            if num or (isinstance(l, str) and isinstance(r, str)) or (isinstance(l, list) and isinstance(r, list)):
                return l + r
            if isinstance(l, Vec3):
                return l + r
        elif op == "-":
            if num or isinstance(l, Vec3):
                return l - r
        elif op == "*":
            if num:
                return l * r
            if isinstance(l, Vec3):
                return l * r
            if isinstance(r, Vec3):
                return r * l
        elif op == "/":
            if num:
                if isinstance(l, int) and isinstance(r, int):
                    return int(l / r)                  # GDScript int division truncates
                return l / r
        elif op == "%":
            if num:
                return l % r
            if isinstance(l, str):
                return l % (tuple(r) if isinstance(r, list) else r)
        elif op in ("==", "!=", "<", ">", "<=", ">="):
            try:
                return {"==": l == r, "!=": l != r, "<": l < r, ">": l > r,
                        "<=": l <= r, ">=": l >= r}[op]
            except TypeError:
                return UNKNOWN
        elif op == "in":
            try:
                return l in r
            except TypeError:
                return UNKNOWN
        return UNKNOWN

    def call(self, fn_ast, args, env):
        if fn_ast[0] == "name":
            name = fn_ast[1]
            if name == "Vector3" and len(args) == 3 and all(isinstance(v, (int, float)) for v in args):
                return Vec3(*args)
            if name == "float":
                return float(args[0]) if isinstance(args[0], (int, float)) else UNKNOWN
            if name == "int":
                return int(args[0]) if isinstance(args[0], (int, float)) else UNKNOWN
            if name == "str":
                return str(args[0]) if isinstance(args[0], (int, float, str)) else UNKNOWN
            if name == "absf":
                return abs(args[0]) if isinstance(args[0], (int, float)) else UNKNOWN
            if name == "maxf":
                return max(args) if all(isinstance(v, (int, float)) for v in args) else UNKNOWN
            if name in self.funcs:
                return self.run_func(name, args)
        return UNKNOWN

    def mcall(self, obj_ast, name, args, env):
        if obj_ast[0] == "name" and name == "new":
            return GNode(obj_ast[1], self.func_stack[-1] if self.func_stack else "<top>")
        here = self.func_stack[-1] if self.func_stack else "<top>"
        if obj_ast == ("name", "PropKit"):
            sig = self.propkit_sigs.get(name)
            if sig and sig[0] in ("Node3D", "Dictionary"):
                return GNode("PropKit." + name, here)
            return UNKNOWN                              # a material, or a void helper
        if obj_ast == ("name", "CharacterKit") and name in self.charkit_names:
            return GNode("CharacterKit." + name, here)
        obj = self.ev(obj_ast, env)
        if name == "size" and isinstance(obj, (list, dict, str)):
            return len(obj)
        if name == "keys" and isinstance(obj, dict):
            return list(obj.keys())
        if name == "append" and isinstance(obj, list):
            obj.append(args[0])
            return None
        if isinstance(obj, str):
            if name == "split" and isinstance(args[0], str):
                return obj.split(args[0])
            if name == "begins_with" and isinstance(args[0], str):
                return obj.startswith(args[0])
            if name == "substr" and isinstance(args[0], int):
                return obj[args[0]:]
        if name == "add_child" and isinstance(obj, GNode) and isinstance(args[0], GNode):
            child = args[0]
            child.parent = obj
            self.children.append(child)
            if child.kind == "Label3D" and isinstance(child.attrs.get("text"), str) and obj.tag is None:
                obj.tag = child.attrs["text"]
            return None
        return UNKNOWN

    ## -- statements
    def run_func(self, name, args):
        params, body = self.funcs[name]
        env = dict(zip(params, args))
        self.func_stack.append(name)
        try:
            self.run_block(body, env)
        except ReturnSignal:
            pass
        self.func_stack.pop()
        return None

    def run_block(self, stmts, env):
        taken = None  # state of the current if/elif chain
        for text, kids in stmts:
            if text.startswith(("if ", "elif ", "else")):
                if text.startswith("if "):
                    cond = self.eval_text(text[3:].rstrip(":"), env)
                    if cond is UNKNOWN:
                        self.gates.append((self.func_stack[-1], text.rstrip(":")))
                    taken = self.truth(cond)
                    if taken:
                        self.run_block(kids, env)
                elif text.startswith("elif "):
                    if not taken:
                        cond = self.eval_text(text[5:].rstrip(":"), env)
                        taken = self.truth(cond)
                        if taken:
                            self.run_block(kids, env)
                else:
                    if not taken:
                        self.run_block(kids, env)
                continue
            taken = None
            self.run_stmt(text, kids, env)

    def run_stmt(self, text, kids, env):
        fn = self.func_stack[-1] if self.func_stack else "<top>"
        if text in ("pass", "return") or text.startswith("return "):
            if text.startswith("return"):
                raise ReturnSignal()
            return
        m = re.match(r"for\s+(\w+)\s+in\s+(.+):$", text)
        if m:
            seq = self.eval_text(m.group(2), env)
            if isinstance(seq, int):
                seq = list(range(seq))
            if not isinstance(seq, list):
                self.unparsed.append((fn, text))
                return
            for item in seq:
                env[m.group(1)] = item
                self.run_block(kids, env)
            return
        m = re.match(r"var\s+(\w+)\s*(?::\s*[\w.]+)?\s*(?::=|=)\s*(.*)$", text)
        if m:
            env[m.group(1)] = self.eval_text(m.group(2), env)
            return
        m = re.match(r"var\s+(\w+)\s*:\s*[\w.]+$", text)
        if m:
            env[m.group(1)] = UNKNOWN
            return
        m = re.match(r"([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\s*=(?!=)\s*(.+)$", text)
        if m:
            target, value = m.group(1).split("."), self.eval_text(m.group(2), env)
            if len(target) == 1:
                (env if target[0] in env else self.globals)[target[0]] = value
                return
            obj = self.lookup(target[0], env)
            if isinstance(obj, GNode) and len(target) == 2:
                if target[1] == "position":
                    obj.pos = value if isinstance(value, Vec3) else UNKNOWN
                else:
                    obj.attrs[target[1]] = value
            return                                      # rotation.y etc.: not a landmark fact
        if kids:                                        # a block we do not model (lambda etc.)
            self.unparsed.append((fn, text))
            return
        # expression statements: the spawn verbs
        m = re.match(r"add_child\((.+)\)$", text)
        if m:
            node = self.eval_text(m.group(1), env)
            if isinstance(node, GNode):
                node.top = True
                self.top.append(node)
            else:
                self.unparsed.append((fn, text))
            return
        m = re.match(r"_dock_body\((\w+),\s*(.+)\)$", text)
        if m:
            node = self.lookup(m.group(1), env)
            # first argument after the node is the plaque text
            args = self.eval_text("[" + m.group(2) + "]", env)
            if isinstance(node, GNode) and isinstance(args, list) and isinstance(args[0], str):
                node.tag = args[0]
            else:
                self.unparsed.append((fn, text))
            return
        m = re.match(r"PropKit\.(\w+)\((.*)\)$", text)
        if m and m.group(1) in self.propkit_sigs and self.propkit_sigs[m.group(1)][0] == "void":
            ret, params = self.propkit_sigs[m.group(1)]
            args = self.eval_text("[" + m.group(2) + "]", env)
            if isinstance(args, list) and "pos" in params and "parent" in params:
                pos = args[params.index("pos")]
                parent_text = self._split_args(m.group(2))[params.index("parent")]
                if parent_text == "self" and isinstance(pos, Vec3):
                    node = GNode("PropKit." + m.group(1), fn)
                    node.pos = pos
                    node.top = True
                    self.top.append(node)
            return                                      # baseboard / door_leaf: geometry on a parent
        m = re.match(r"(_\w+)\((.*)\)$", text)
        if m and m.group(1) in self.funcs:
            if m.group(1) in self.GEOMETRY_FUNCS:
                return
            args = self.eval_text("[" + m.group(2) + "]", env) if m.group(2).strip() else []
            if not isinstance(args, list):
                self.unparsed.append((fn, text))
                return
            self.run_func(m.group(1), args)
            return
        # anything else (connect, add_to_group, setup, register_station...)
        self.eval_text(text, env)

    @staticmethod
    def _split_args(s):
        """split an argument list at depth-0 commas (strings and brackets respected)"""
        out, buf, d, q = [], [], 0, None
        for c in s:
            if q:
                buf.append(c)
                if c == q:
                    q = None
            elif c in "\"'":
                q = c
                buf.append(c)
            elif c in "([{":
                d += 1
                buf.append(c)
            elif c in ")]}":
                d -= 1
                buf.append(c)
            elif c == "," and d == 0:
                out.append("".join(buf).strip())
                buf = []
            else:
                buf.append(c)
        if buf:
            out.append("".join(buf).strip())
        return out

    def excluded(self, kind):
        return kind in self.EXCLUDED_KINDS or bool(self.EXCLUDED_KIND.search(kind))


## --- run it over the builder ----------------------------------------------
def _propkit_signatures():
    sigs = {}
    src = open(os.path.join(ROOT, "scripts", "prop_kit.gd"), encoding="utf-8").read()
    for m in re.finditer(r"^static func (\w+)\((.*?)\)\s*->\s*(\w+):", src, re.M):
        params = [p.split(":")[0].strip() for p in m.group(2).split(",") if p.strip()]
        sigs[m.group(1)] = (m.group(3), params)
    return sigs


def _charkit_names():
    src = open(os.path.join(ROOT, "scripts", "character_kit.gd"), encoding="utf-8").read()
    return set(re.findall(r"^static func (\w+)\(", src, re.M))


def _class_scripts():
    """class_name → scripts/<file>.gd, plus each class's `extends` parent."""
    scripts, parents = {}, {}
    sdir = os.path.join(ROOT, "scripts")
    for fn in sorted(os.listdir(sdir)):
        if not fn.endswith(".gd"):
            continue
        head = open(os.path.join(sdir, fn), encoding="utf-8").read(400)
        cm = re.search(r"^class_name\s+(\w+)", head, re.M)
        em = re.search(r"^extends\s+(\w+)", head, re.M)
        if cm:
            scripts[cm.group(1)] = "scripts/" + fn
            parents[cm.group(1)] = em.group(1) if em else ""
    return scripts, parents


def _tier(kind, parents):
    if kind.startswith(("PropKit.", "CharacterKit.")):
        return "propkit"
    if kind not in parents:
        return "inline"
    k = kind
    while k in parents:
        if k == "Interactable":
            return "interactable"
        k = parents[k]
    return "scripted"


def _fmt(v):
    s = "%.4f" % v
    s = s.rstrip("0")
    return s + "0" if s.endswith(".") else s


propkit_sigs = _propkit_signatures()
builder = Builder(wb, propkit_sigs, _charkit_names())
builder.run_func("_ready", [])
class_scripts, class_parents = _class_scripts()

ROOM_TOL = builder.globals["WALL_T"] / 2.0 + 0.01


def rooms_at(x, z):
    hits = []
    for name, (cx, cz, sx, sz) in builder.globals["ROOMS"].items():
        if abs(x - cx) <= sx / 2.0 + ROOM_TOL and abs(z - cz) <= sz / 2.0 + ROOM_TOL:
            hits.append(name)
    return "|".join(hits) if hits else "OPEN"


def landmark_name(n):
    name = n.tag
    if name is None:
        for attr in ("door_label", "sign_text", "label_text", "slate_text"):
            if isinstance(n.attrs.get(attr), str):
                name = n.attrs[attr]
                break
    if name is None:
        name = n.kind
    a = n.attrs
    if n.kind == "LogStation" and isinstance(a.get("station_name"), str):
        name = "%s · %s" % (name, a["station_name"])
    elif n.kind == "KeyItem" and isinstance(a.get("key_id"), str):
        name = "%s · %s" % (name, a["key_id"])
    elif n.kind == "AssetPickup" and isinstance(a.get("asset_id"), str):
        name = "%s · %s" % (name, a["asset_id"])
    elif n.kind == "ReadableProp" and isinstance(a.get("doc_id"), str) and isinstance(a.get("label"), str):
        name = "%s · %s" % (a["doc_id"], a["label"])
    return name


# positions: MonitorRig stands at monitor_position (monitor_rig.gd:43-57)
for n in builder.top:
    if n.pos is None and isinstance(n.attrs.get("monitor_position"), Vec3):
        n.pos = n.attrs["monitor_position"]

candidates = [n for n in builder.top if not builder.excluded(n.kind)]
positionless = [n for n in candidates if n.pos is None]
placed = [n for n in candidates if isinstance(n.pos, Vec3)]
unplaced = [n for n in candidates if n.pos is UNKNOWN]

# floating Label3D tags: name the node at the same x,z from the same function
dropped_labels = []
landmarks = []
labels = [n for n in placed if n.kind == "Label3D"]
others = [n for n in placed if n.kind != "Label3D"]
for lab in labels:
    text = lab.attrs.get("text")
    if not isinstance(text, str):
        dropped_labels.append(lab)
        continue
    host = [o for o in others if o.func == lab.func and (o.pos.x, o.pos.z) == (lab.pos.x, lab.pos.z)]
    if host:
        if host[0].tag is None:
            host[0].tag = text
    else:
        lab.tag = text
        others.append(lab)
landmarks = [n for n in placed if n in others]  # source order preserved

lm_rows = []
for n in landmarks:
    if n.kind.startswith("PropKit."):
        script = "scripts/prop_kit.gd"
    elif n.kind.startswith("CharacterKit."):
        script = "scripts/character_kit.gd"
    elif n.kind in class_scripts:
        script = class_scripts[n.kind]
    else:
        script = "scripts/world_builder.gd"            # Node3D/Label3D assembled inline
    lm_rows.append([landmark_name(n), rooms_at(n.pos.x, n.pos.z), _fmt(n.pos.x), _fmt(n.pos.z),
                    n.kind, script])

## tripwires: arithmetic before trust
_kinds_rows = {r[4] for r in lm_rows}
_kinds_children = {c.kind for c in builder.children}
_kinds_positionless = {n.kind for n in positionless}
_seen_classes = set(re.findall(r"\b([A-Z]\w+)\.new\(\)", wb)) - {k for k in re.findall(r"\b([A-Z]\w+)\.new\(\)", wb) if builder.excluded(k)}
_missing = sorted(k for k in _seen_classes if k not in _kinds_rows | _kinds_children | _kinds_positionless)
assert not _missing, "classes instantiated in world_builder.gd but never followed: %s" % _missing
_seen_factories = {"PropKit." + f for f in re.findall(r"PropKit\.(\w+)\(", wb)
                   if propkit_sigs.get(f, ("",))[0] in ("Node3D", "Dictionary")}
_missing_f = sorted(f for f in _seen_factories if f not in _kinds_rows | _kinds_children)
assert not _missing_f, "PropKit factories called in world_builder.gd but never followed: %s" % _missing_f
assert not unplaced, "landmarks with a position the evaluator could not compute: %s" % [(n.kind, n.func) for n in unplaced]
_by_kind = {}
for r in lm_rows:
    _by_kind[r[4]] = _by_kind.get(r[4], 0) + 1
assert _by_kind.get("LogStation") == len(stations), "stations: %r vs %d" % (_by_kind.get("LogStation"), len(stations))
assert _by_kind.get("MonitorRig") == len(monitors), "monitors: %r vs %d" % (_by_kind.get("MonitorRig"), len(monitors))
_hinged = [d for d in doors if d[6] != ""]
_door_labels = {r[0] for r in lm_rows if r[4] == "CompoundDoor"}
for d in _hinged:
    assert "%s / %s" % (d[0], d[1]) in _door_labels, "door table row without a CompoundDoor landmark: %s" % (d,)
assert _by_kind.get("KeyItem") == len(re.findall(r"^\s+_spawn_key\(", wb, re.M)), "keys"
assert _by_kind.get("ReadableProp") == len(re.findall(r'\["(D\d+)",\s*"[^"]+",\s*Vector3\(', wb)), "readables"
_dock_loop = re.search(r"func _spawn_dock_task.*?for i in (\d+):", wb, re.S)
assert _by_kind.get("DockChum") == int(_dock_loop.group(1)), "dock chums"
_keyset = [(r[4], r[2], r[3]) for r in lm_rows]
assert len(_keyset) == len(set(_keyset)), "duplicate (kind, x, z) landmark rows"
assert all(r[1] != "OPEN" for r in lm_rows), "landmark outside every room: %s" % [r for r in lm_rows if r[1] == "OPEN"]
assert all(os.path.exists(os.path.join(ROOT, r[5])) for r in lm_rows), "landmark script path missing"

with open(os.path.join(OUT, "Landmarks.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["name", "room", "x", "z", "kind", "script"])
    w.writerows(lm_rows)

_tiers = {}
for r in lm_rows:
    t = _tier(r[4], class_parents)
    _tiers[t] = _tiers.get(t, 0) + 1
print("LANDMARKS rows=%d kinds=%d tiers=%s" % (
    len(lm_rows), len(_by_kind), " ".join("%s=%d" % kv for kv in sorted(_tiers.items()))))
print("LANDMARKS by kind: " + ", ".join("%s=%d" % kv for kv in sorted(_by_kind.items())))
print("LANDMARK-POSITIONLESS (systems, not written): " + ", ".join(
    "%s@%s" % (n.kind, n.func) for n in positionless))
print("LANDMARK-GATES (conditions unknown here, taken as true = fresh save, full game):")
for fn, cond in builder.gates:
    print("  %s: %s" % (fn, cond))
print("LANDMARK-DROPPED-LABELS (runtime text): " + ", ".join(
    "%s@%s" % (n.kind, n.func) for n in dropped_labels))
print("LANDMARK-UNPARSED (statements the evaluator did not follow):")
for fn, text in builder.unparsed:
    print("  %s: %s" % (fn, text[:110]))

print("DATA-EXTRACTED rooms=%d doors=%d stations=%d monitors=%d demo=%d timings=%d text=%d landmarks=%d"
      % (len(rooms), len(doors), len(stations), len(monitors), len(demo), len(rows), len(keys), len(lm_rows)))
