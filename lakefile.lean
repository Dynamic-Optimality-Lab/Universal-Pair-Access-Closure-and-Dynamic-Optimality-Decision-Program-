-- lakefile.lean — SPLAY-AM-DECIDE-v0.4 (dependency-free; compile-unverified pending Lean toolchain install at Phase-1 execution)
import Lake
open Lake DSL

package splay_am_decide where
  version := v!"0.4.0"
  edition := "2022-12-08"

@[default_target]
lean_lib SplayDecide where
  srcDir := "lean"
