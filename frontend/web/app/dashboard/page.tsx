'use client'

import { useState } from 'react'
import DashboardStats from '@/components/DashboardStats'
import RecentOrders from '@/components/RecentOrders'
import UserActivity from '@/components/UserActivity'
import RevenueChart from '@/components/RevenueChart'
import TopProducts from '@/components/TopProducts'

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-2xl font-bold text-gray-900">
            Admin Dashboard
          </h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats */}
        <DashboardStats />

        {/* Charts */}
        <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
          <RevenueChart />
          <UserActivity />
        </div>

        {/* Tables */}
        <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
          <RecentOrders />
          <TopProducts />
        </div>
      </main>
    </div>
  )
}
