'use client'

import { useQuery } from '@tanstack/react-query'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

async function fetchRevenueData() {
  // TODO: Replace with actual API call
  return [
    { month: 'Jan', revenue: 450000, orders: 1200 },
    { month: 'Feb', revenue: 520000, orders: 1400 },
    { month: 'Mar', revenue: 480000, orders: 1300 },
    { month: 'Apr', revenue: 610000, orders: 1600 },
    { month: 'May', revenue: 550000, orders: 1500 },
    { month: 'Jun', revenue: 670000, orders: 1800 },
  ]
}

export default function RevenueChart() {
  const { data: revenueData } = useQuery({
    queryKey: ['revenue-data'],
    queryFn: fetchRevenueData,
  })

  if (!revenueData) return <div>Loading...</div>

  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        Revenue Trend
      </h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={revenueData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip
            formatter={(value: number) => `₹${value.toLocaleString()}`}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="revenue"
            stroke="#6366f1"
            strokeWidth={2}
            name="Revenue"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
