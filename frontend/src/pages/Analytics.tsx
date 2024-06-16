import { ThreeDots } from 'react-loader-spinner';
import {
  Area,
  AreaChart,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import useSWR, { Fetcher } from 'swr';
import Refresh from '../components/Refresh';

interface VisitorsData {
  date: string;
  visitors: number;
}

const fetcher: Fetcher<VisitorsData[], string> = async () => {
  const res = {
    data: {
      visitors: [
        { date: '2024-05-10', visitors: Math.floor(Math.random() * 10) },
        { date: '2024-05-11', visitors: Math.floor(Math.random() * 10) },
        { date: '2024-05-12', visitors: Math.floor(Math.random() * 10) },
        { date: '2024-05-13', visitors: Math.floor(Math.random() * 10) },
        { date: '2024-05-14', visitors: Math.floor(Math.random() * 10) },
        { date: '2024-05-15', visitors: Math.floor(Math.random() * 10) },
        { date: '2024-05-16', visitors: Math.floor(Math.random() * 10) },
      ],
    },
  };

  await new Promise((res) => setTimeout(res, 1500));

  return res.data.visitors as VisitorsData[];
};

function Analytics() {
  const { data, isLoading, isValidating, mutate } = useSWR('visitors', fetcher);

  return (
    <main className="flex flex-col items-center px-6 flex-1">
      <h2 className="text-2xl font-medium">Analytics</h2>
      {isLoading && (
        <div className="my-auto flex flex-col items-center gap-2">
          <ThreeDots />
          <p className="italic">Loading analytics...</p>
        </div>
      )}
      {!isLoading && <Refresh mutate={mutate} isValidating={isValidating} />}
      {!isLoading && !data?.length && <p>Try again later 😬</p>}
      {!isLoading && !!data?.length && (
        <div className="w-full max-w-6xl text-[#2a5e87] my-auto">
          <ResponsiveContainer width="100%" height={400}>
            <AreaChart
              data={data}
              margin={{ top: 5, right: 30, bottom: 5, left: 0 }}
            >
              <Legend verticalAlign="top" height={30} />
              <XAxis dataKey="date" />
              <YAxis />
              <Area type="monotone" dataKey="visitors" />
              <Tooltip />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}
    </main>
  );
}

export default Analytics;
