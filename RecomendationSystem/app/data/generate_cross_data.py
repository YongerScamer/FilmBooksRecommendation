import pandas as pd
import numpy as np
import argparse
import random
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer


def generate_cross_domain_by_genre(book_file, movie_file, output_file,
                                   threshold=0.4, num_negative=5):
    books_df = pd.read_csv(book_file)
    movies_df = pd.read_csv(movie_file)

    if 'BookID' not in books_df.columns or 'BookGenre' not in books_df.columns:
        raise ValueError("books_df must have 'BookID' and 'BookGenre' columns")
    if 'MovieID' not in movies_df.columns or 'MovieGenre' not in movies_df.columns:
        raise ValueError("movies_df must have 'MovieID' and 'MovieGenre' columns")

    books_df['BookGenre'] = books_df['BookGenre'].apply(lambda x: x.split('|'))
    movies_df['MovieGenre'] = movies_df['MovieGenre'].apply(lambda x: x.split('|'))

    mlb = MultiLabelBinarizer()
    all_genres = books_df['BookGenre'].tolist() + movies_df['MovieGenre'].tolist()
    mlb.fit(all_genres)

    book_genres_vec = mlb.transform(books_df['BookGenre'])
    movie_genres_vec = mlb.transform(movies_df['MovieGenre'])

    sim_matrix = cosine_similarity(book_genres_vec, movie_genres_vec)

    pairs = []
    for i, book_id in enumerate(books_df['BookID']):
        sims = sim_matrix[i]
        sorted_indices = np.argsort(-sims)
        for j in sorted_indices:
            movie_id = movies_df.iloc[j]['MovieID']
            score = sims[j]
            if score >= threshold:
                pairs.append((book_id, movie_id, 1))
            else:
                break

        negatives = 0
        attempts = 0
        while negatives < num_negative and attempts < 50:
            j = random.randint(0, len(movies_df) - 1)
            score = sims[j]
            if score < threshold:
                movie_id = movies_df.iloc[j]['MovieID']
                pairs.append((book_id, movie_id, 0))
                negatives += 1
            attempts += 1

    df = pd.DataFrame(pairs, columns=['Target', 'Context', 'Label'])
    df.to_csv(output_file, index=False)
    print(f"Cross-domain dataset saved to {output_file}, total pairs: {len(df)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--books', type=str, required=True, help='Path to book genres CSV')
    parser.add_argument('--movies', type=str, required=True, help='Path to movie genres CSV')
    parser.add_argument('--output', type=str, required=True, help='Output CSV path')
    parser.add_argument('--threshold', type=float, default=0.4, help='Cosine similarity threshold for positive match')
    parser.add_argument('--negatives', type=int, default=5, help='Number of negative examples per book')
    args = parser.parse_args()

    generate_cross_domain_by_genre(
        book_file=args.books,
        movie_file=args.movies,
        output_file=args.output,
        threshold=args.threshold,
        num_negative=args.negatives
    )
