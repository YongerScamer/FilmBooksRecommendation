import tensorflow as tf

class ContentRecommender(tf.keras.Model):
    def __init__(self, content_dim, hidden_dim=64):
        super().__init__()
        self.dense1 = tf.keras.layers.Dense(hidden_dim, activation='relu')
        self.dense2 = tf.keras.layers.Dense(hidden_dim // 2, activation='relu')
        self.output_layer = tf.keras.layers.Dense(1)

    def call(self, content_features):
        x = self.dense1(content_features)
        x = self.dense2(x)
        return self.output_layer(x)

    def train_model(self, features, ratings, epochs=5, lr=0.001):
        optimizer = tf.keras.optimizers.Adam(lr)
        loss_fn = tf.keras.losses.MeanSquaredError()

        dataset = tf.data.Dataset.from_tensor_slices((features, ratings)).shuffle(10000).batch(64)

        for epoch in range(epochs):
            total_loss = 0
            for x, y in dataset:
                with tf.GradientTape() as tape:
                    preds = self(x)
                    loss = loss_fn(y, preds)
                grads = tape.gradient(loss, self.trainable_variables)
                optimizer.apply_gradients(zip(grads, self.trainable_variables))
                total_loss += loss.numpy()
            print(f"Content Model Epoch {epoch+1}: Loss = {total_loss:.4f}")

    def get_recommendations(self, content_features_all, movie_index_to_title, top_k=10):
        preds = self(tf.constant(content_features_all)).numpy().flatten()
        preds = (preds - preds.min()) / (preds.max() - preds.min() + 1e-10)
        top_indices = preds.argsort()[::-1][:top_k]
        return [(movie_index_to_title[i], float(f"{preds[i]:.8f}")) for i in top_indices]
    
    def save_model(self, path="content_model_weights"):
        self.save_weights(path)

    def load_model(self, path="content_model_weights"):
        self.load_weights(path)