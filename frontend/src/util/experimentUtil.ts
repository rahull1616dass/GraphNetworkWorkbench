import * as trainTestSplit from 'train-test-split'
import type { Network } from '../definitions/network'

export function train_test_split(network: Network, seed: number, trainPercentage: number): Network{
    const [train_indices, test_indices] = trainTestSplit(network.nodes, trainPercentage, seed, true)
    console.log(train_indices)
    network.nodes.map((node, index) => {
        /*
        2 and 1 since the color key does not accept boolean values or 0-indexed values.
        TODO: Change the vegaEmbed VisSpec color key to accept boolean values or 0-indexed values 
        or do sth about this, wtf is this travesty
        */
        if (train_indices.includes(index)) {
            node.is_train = 2
        } else {
            node.is_train = 1
        }
    })
    return network
}