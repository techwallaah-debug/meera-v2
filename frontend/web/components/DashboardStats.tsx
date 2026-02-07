'use client'

import { useQuery } from '@tanstack/react-query'
import { TrendingUp, Users, ShoppingCart, DollarSign } from 'lucide-react'

async function fetchStats() {
  // TODO: Replace with actual API call
  return {
    totalUsers: 12543,
    totalOrders: 8921,
    totalRevenue: 2456789,
    growthRate: 12.5,
  }
}

export default function DashboardStats() {
  const { data: stats } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: fetchStats,
  })

  if (!stats) return <div>Loading...</div>

  const statCards = [
    {
      name: 'Total Users',
      value: stats.totalUsers.toLocaleString(),
      icon: Users,
      change: `+${stats.growthRate}%`,
      changeType: 'increase' as const,
    },
    {
      name: 'Total Orders',
      value: stats.totalOrders.toLocaleString(),
      icon: ShoppingCart,
      change: `+${stats.growthRate}%`,
      changeType: 'increase' as const,
    },
    {
      name: 'Total Revenue',
      value: `₹${(stats.totalRevenue / 100000).toFixed(2)}L`,
      icon: DollarSign,
      change: `+${stats.growthRate}%`,
      changeType: 'increase' as const,
    },
    {
      name: 'Growth Rate',
      value: `${stats.growthRate}%`,
      icon: TrendingUp,
      change: 'vs last month',
      changeType: 'neutral' as const,
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {statCards.map((stat) => (
        <div
          key={stat.name}
          className="bg-white rounded-lg shadow p-6 border border-gray-200"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">{stat.name}</p>
              <p className="text-2xl font-bold text-gray-900 mt-2">
                {stat.value}
              </p>
              <p
                className={`text-sm mt-2 ${
                  stat.changeType === 'increase'
                    ? 'text-green-600'
                    : stat.changeType === 'decrease'
                    ? 'text-red-600'
                    : 'text-gray-600'
                }`}
              >
                {stat.change}
              </p>
            </div>
            <div className="p-3 bg-indigo-100 rounded-lg">
              <stat.icon className="h-6 w-6 text-indigo-600" />
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
