-- lakefile.lean — SPLAY-AM-DECIDE-v0.4 (dependency-free; compile-unverified pending Lean toolchain install at Phase-1 execution)
import Lake
open Lake DSL

package splay_am_decide where
  version := v!"0.4.0"

@[default_target]
lean_lib SplayDecide where
  srcDir := "lean"
  roots := #[`Frozen.SplayDefs, `Frozen.MSTC0002Defs, `Frozen.Statements,
    `Proofs.Injection, `Proofs.Locality, `Proofs.Preservation, `Proofs.Boundary,
    `Proofs.Constants, `Proofs.Repayment, `Proofs.Integrability,
    `Proofs.Composition, `Proofs.Telescope, `Proofs.Family]

lean_exe agree where
  root := `Agree
  srcDir := "lean"
