import { useEffect, useState } from 'react';
import { useAuthState } from 'react-firebase-hooks/auth';
import { useCollectionData } from 'react-firebase-hooks/firestore';
import {
  addDoc,
  collection,
  deleteDoc,
  query,
  setDoc,
  where,
} from 'firebase/firestore';
import { Rating, RatingChange } from '@smastrom/react-rating';
import { auth, db } from '../firebase';
import TMDBMovie from '../types/TMDBMovie';
import posterPlaceholder from '../assets/poster_placeholder.svg';

interface RateMovieProps {
  movie: TMDBMovie;
}

const ratingsRef = collection(db, 'ratings');

function RateMovie({ movie }: RateMovieProps) {
  const [user] = useAuthState(auth);

  if (!user) throw new Error('No user');

  const [rating, setRating] = useState<number | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const q = query(
    ratingsRef,
    where('userId', '==', user.uid),
    where('movieId', '==', movie.id),
  );

  const [values, isLoading, , snapshot] = useCollectionData<{
    userId?: string;
    movieId?: number;
    rating?: number;
  }>(q);

  const dbRating = values?.[0]?.rating;
  const docRef = snapshot?.docs[0]?.ref;

  useEffect(() => {
    setRating(dbRating || null);
  }, [dbRating]);

  const handleChange: RatingChange = async (value: number) => {
    setIsProcessing(true);

    const data = {
      userId: user.uid,
      movieId: movie.id,
      rating: value,
    };

    try {
      if (docRef) {
        if (value !== 0) {
          await setDoc(docRef, data);
        } else {
          await deleteDoc(docRef);
        }
      } else {
        await addDoc(ratingsRef, data);
      }
    } catch (error) {
      console.log(error);
    } finally {
      setIsProcessing(false);
    }
  };

  const posterUrl = `https://image.tmdb.org/t/p/w154${movie.poster_path}`;

  return (
    <article className="flex flex-col items-center w-[250px]">
      <img
        src={movie.poster_path ? posterUrl : posterPlaceholder}
        alt={movie.title}
        className="w-[154px] h-[231px] object-contain mb-2"
      />
      <h3 className="my-auto text-lg text-center text-gray-200 font-medium">
        {movie.title}
      </h3>
      <Rating
        value={rating || 0}
        onChange={handleChange}
        isDisabled={isLoading || isProcessing}
        className="max-w-[150px] mt-2"
      />
    </article>
  );
}

export default RateMovie;
