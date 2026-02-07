'use client'

import { useQuery } from '@tanstack/react-query'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

async function fetchUserActivity() {
  // TODO: Replace with actual API call
  return [
    { day: 'Mon', active: 1200, new: 150 },
    { day: 'Tue', active: 1350, new: 180 },
    { day: 'Wed', active: 1100, new: 140 },
    { day: 'Thu', active: 1450, new: 200 },
    { day: 'Fri', active: 1600, new: 220 },
    { day: 'Sat', active: 1800, new: 250 },
    { day: 'Sun', active: 1700, new: 230 },
  ]
}

export default function UserActivity() {
  const { data: activityData } = useQuery({
    queryKey: ['user-activity'],
    queryFn: fetchUserActivity,
  })

  if (!activityData) return <div>Loading...</div>

  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        User Activity
      </h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={activityData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="day" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="active" fill="#6366f1" name="Active Users" />
          <Bar dataKey="new" fill="#10b981" name="New Users" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
