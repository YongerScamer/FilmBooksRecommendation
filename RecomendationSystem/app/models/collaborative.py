import tensorflow as tf

class CollaborativeRecommender(tf.keras.Model):
    def __init__(self, num_users, num_movies, embedding_dim=64, hidden_dim=64):
        super().__init__()
        self.user_embedding = tf.keras.layers.Embedding(num_users, embedding_dim)
        self.movie_embedding = tf.keras.layers.Embedding(num_movies, embedding_dim)
        self.dense1 = tf.keras.layers.Dense(hidden_dim, activation='relu')
        self.dense2 = tf.keras.layers.Dense(hidden_dim // 2, activation='relu')
        self.output_layer = tf.keras.layers.Dense(1)

    def call(self, inputs):
        user_ids, movie_ids = inputs
        user_vec = self.user_embedding(user_ids)
        movie_vec = self.movie_embedding(movie_ids)
        x = tf.concat([user_vec, movie_vec], axis=-1)
        x = self.dense1(x)
        x = self.dense2(x)
        return self.output_layer(x)
    def train_collaborative_model(self, user_ids, movie_ids, ratings, epochs=5, lr=0.001):
        optimizer = tf.keras.optimizers.Adam(lr)
        loss_fn = tf.keras.losses.MeanSquaredError()

        dataset = tf.data.Dataset.from_tensor_slices(((user_ids, movie_ids), ratings)).shuffle(10000).batch(64)

        for epoch in range(epochs):
            total_loss = 0
            for (u, m), r in dataset:
                with tf.GradientTape() as tape:
                    preds = self((u, m))
                    loss = loss_fn(r, preds)
                grads = tape.gradient(loss, self.trainable_variables)
                optimizer.apply_gradients(zip(grads, self.trainable_variables))
                total_loss += loss.numpy()
            print(f"Collaborative Model Epoch {epoch+1}: Loss = {total_loss:.4f}")

    def recommend_collaborative(self, user_id, all_movie_ids, movie_index_to_title, top_k=10):
        user_tensor = tf.constant([user_id] * len(all_movie_ids))
        movie_tensor = tf.constant(all_movie_ids)

        preds = self((user_tensor, movie_tensor)).numpy().flatten()
        preds = (preds - preds.min()) / (preds.max() - preds.min() + 1e-10)
        top_indices = preds.argsort()[::-1][:top_k]
        return [(movie_index_to_title[i], float(f"{preds[i]:.8f}")) for i in top_indices]
    
    def save_model(self, path="collab_model_weights"):
        self.save_weights(path)

    def load_model(self, path="collab_model_weights"):
        self.load_weights(path)
