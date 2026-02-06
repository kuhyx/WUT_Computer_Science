import { RotatingLines } from 'react-loader-spinner';

interface RefreshProps {
  mutate: () => void;
  isValidating: boolean;
}

function Refresh({ mutate, isValidating }: RefreshProps) {
  return (
    <div className="flex relative">
      <button
        onClick={() => mutate()}
        disabled={isValidating}
        className={`mt-10 mb-10 flex items-center gap-2 border rounded-full py-2 px-4 border-gray-400 hover:bg-gray-700 duration-100 ${isValidating ? 'cursor-wait' : ''}`}
      >
        {isValidating ? 'Refreshing...' : 'Refresh'}
      </button>
      {isValidating && (
        <div className="absolute -right-2 translate-x-full top-1/2 -translate-y-1/2">
          <RotatingLines width="24" strokeColor="#fff" />
        </div>
      )}
    </div>
  );
}

export default Refresh;
