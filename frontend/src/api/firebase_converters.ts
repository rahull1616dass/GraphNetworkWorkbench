import { Metadata } from "../definitions/network"

export const metadataConverter = {
    toFirestore: function (metadata: Metadata) {
      return {
        id: metadata.id,
        name: metadata.name,
        description: metadata.description,
        color: metadata.color
      }
    },
    fromFirestore: function (snapshot, options) {
      const data = snapshot.data(options)
      return new Metadata(
        data.id,
        data.name,
        data.description,
        data.color
      )
    }
  }