#include <dmlc/logging.h>
#include <gtest/gtest.h>
#include <tvm/tvm.h>

TEST(Expr, Basic) {
  using namespace tvm;
  Var x("x");
  auto z = max(x + 1 + 2, 100);
  NodeRef tmp = z;
  Expr zz(tmp.node_);
  std::ostringstream os;
  os << z;
  CHECK(zz.same_as(z));
  CHECK(os.str() == "max(((x + 1) + 2), 100)");
}


TEST(ExprNodeRef, Basic) {
  using namespace tvm;
  Var x("x");
  Expr z = max(x + 1 + 2, 100);
  const ir::Max* op = z.as<ir::Max>();
  CHECK(NodeRef(op->GetNodePtr()).same_as(z));
}


int main(int argc, char ** argv) {
  testing::InitGoogleTest(&argc, argv);
  testing::FLAGS_gtest_death_test_style = "threadsafe";
  return RUN_ALL_TESTS();
}
