# Symmetry sieve

## Idea

Most machine learning problems have inputs with a certain symmetry in them. Unless you're google, your dataset is not large enough to fully capture the sub-space the inputs live in. A very common approach is therefore to augment your dataset with transformations you know should not affect the output. However, this is not a particularly scalable approach. Different datasets may exhibit the same symmetries and even on the same dataset hyperparameter search means you'll be training your model many times over, re-learning the same symmetries over and over again.

Is there instead a way to train a neural network on *symmetry* only? If so, we could first transform our data using this network, then all further training would happen on this transformed output. If this method were effective, training time could potentially be a lot shorter and furthermore, by inspecting the "symmetry sieve" we could get inspiration for new network layers that obey certain symmetries, like convolutions.

## Initial thoughts on implementation

Feed the network with four inputs, generated from two samples of random noise, each augmented with two different transformations. Then run each pair (6 of them; two from the same sample and four from different samples) through a discriminator with an appropriate loss. Given the imbalance of pairings, it will probably make sense to weight them. `TODO: Look at the literature for contrastive loss`
