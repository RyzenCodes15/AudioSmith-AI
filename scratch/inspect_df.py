import torch
from df.enhance import init_df
model, state, _ = init_df()
print("Model type:", type(model))
# inspect forward signature
import inspect
print(inspect.signature(model.forward))
