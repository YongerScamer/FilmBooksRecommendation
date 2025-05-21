import tensorflow as tf
import numpy as np

class SkipGram(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim):
        super(SkipGram, self).__init__()
        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim, name="movie_embedding")
    
    def call(self, inputs):
        return self.embedding(inputs)

    def train_model(self, dataset, epochs=10, learning_rate=0.01):
        optimizer = tf.keras.optimizers.Adam(learning_rate)
        loss_fn = tf.keras.losses.BinaryCrossentropy(from_logits=True)
        
        for epoch in range(epochs):
            total_loss = 0
            for target, context, label in dataset:
                with tf.GradientTape() as tape:
                    target_emb = self(tf.convert_to_tensor([target]))
                    context_emb = self(tf.convert_to_tensor([context]))
                    dot_product = tf.reduce_sum(target_emb * context_emb, axis=-1)
                    loss = loss_fn(tf.convert_to_tensor([label], dtype=tf.float32), dot_product)
                grads = tape.gradient(loss, self.trainable_variables)
                optimizer.apply_gradients(zip(grads, self.trainable_variables))
                total_loss += loss.numpy()
            print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")

    def get_recommendations(self, input_vector, movie_index_to_title, top_k=10):
        embeddings = self.embedding.weights[0].numpy()
        norms = np.linalg.norm(embeddings, axis=1) * np.linalg.norm(input_vector)
        similarities = np.dot(embeddings, input_vector) / (norms + 1e-10)
        similarities = (similarities - similarities.min()) / (similarities.max() - similarities.min() + 1e-10)
        
        top_indices = np.argsort(similarities)[::-1][:top_k]
        return [
            (movie_index_to_title[i], float(f"{similarities[i]:.8f}"))
            for i in top_indices
        ]
    def save_model(self, path="skipgram_weights"):
        self.save_weights(path)

    def load_model(self, path="skipgram_weights"):
        self.load_weights(path)
