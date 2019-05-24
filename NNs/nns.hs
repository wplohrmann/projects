-- Every network has an input and an output.
-- Bigger network are built up from smaller ones.
-- This happens through composition. Essentially,
-- networks are just functions. However, we need to somehow
-- store the structure of the network so we can derive both the forward and backward 
-- pass. At the same time, we'd like to operate on these seemlessly as if they were functions
-- without them actually being functions.
data Neuron = Const Float | Connected [(Float, Neuron)] deriving Show

forward :: Neuron -> Float
forward (Const x) = x
forward (Connected inputs) = sum $ map (\(weight, neuron) -> weight * (forward neuron)) inputs

simpleNet :: Neuron
simpleNet = Connected [(1.3, Const 2)]

denseNet :: [Neuron]
denseNet = replicate 5 (Connected (replicate 2 (1.3, Const 3)))

main :: IO ()
main = do
    print $ forward simpleNet
    print $ map forward denseNet
