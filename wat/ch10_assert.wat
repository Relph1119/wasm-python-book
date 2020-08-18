(module
  (func (export "assert_true") (param i32)
    (if (i32.eqz (local.get 0))
      (unreachable)
    )
  )
  (func (export "assert_false") (param i32)
    (if (i32.ne (local.get 0) (i32.const 0))
      (unreachable)
    )
  )
  (func (export "assert_eq_i32") (param i32 i32)
    (if (i32.ne (local.get 0) (local.get 1))
      (unreachable)
    )
  )
  (func (export "assert_eq_i64") (param i64 i64)
    (if (i64.ne (local.get 0) (local.get 1))
      (unreachable)
    )
  )
  (func (export "assert_eq_f32") (param f32 f32)
    (if (f32.ne (local.get 0) (local.get 1))
      (unreachable)
    )
  )
  (func (export "assert_eq_f64") (param f64 f64)
    (if (f64.ne (local.get 0) (local.get 1))
      (unreachable)
    )
  )
)