import tvm
import numpy as np

@tvm.register_dltensor
class MyTensorView(object):
    def __init__(self, arr):
        self.arr = arr

    @property
    def _dltensor_addr(self):
        return self.arr._dltensor_addr

def test_dltensor_compatible():
    dtype = 'int64'
    n = tvm.var('n')
    Ab = tvm.decl_buffer((n,), dtype)
    i = tvm.var('i')
    ib = tvm.ir_builder.create()
    A = ib.buffer_ptr(Ab)
    with ib.for_range(0, n - 1, "i") as i:
        A[i + 1] = A[i] + 1
    stmt = ib.get()
    fapi = tvm.ir_pass.MakeAPI(stmt, "arange", [Ab], 0)
    fapi = tvm.ir_pass.LowerPackedCall(fapi)
    f = tvm.codegen.build_module(fapi, "stackvm")
    a = tvm.nd.array(np.zeros(10, dtype=dtype))
    aview = MyTensorView(a)
    f(aview)
    np.testing.assert_equal(a.asnumpy(), np.arange(a.shape[0]))

if __name__ == "__main__":
    test_dltensor_compatible()
