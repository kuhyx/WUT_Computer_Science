import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: 'AIzaSyAF34ovW0qaDlV68sbpCjylz4TQ0he_XEM',
  authDomain: 'movie-recommendation-2024.firebaseapp.com',
  projectId: 'movie-recommendation-2024',
  storageBucket: 'movie-recommendation-2024.appspot.com',
  messagingSenderId: '777010585410',
  appId: '1:777010585410:web:7db1436b72879d512032db',
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

export { auth, db };
