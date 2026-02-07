'use client'

import { useQuery } from '@tanstack/react-query'

async function fetchTopProducts() {
  // TODO: Replace with actual API call
  return [
    { id: 1, name: 'Product A', sales: 1250, revenue: 312500 },
    { id: 2, name: 'Product B', sales: 980, revenue: 245000 },
    { id: 3, name: 'Product C', sales: 750, revenue: 187500 },
    { id: 4, name: 'Product D', sales: 620, revenue: 155000 },
    { id: 5, name: 'Product E', sales: 540, revenue: 135000 },
  ]
}

export default function TopProducts() {
  const { data: products } = useQuery({
    queryKey: ['top-products'],
    queryFn: fetchTopProducts,
  })

  if (!products) return <div>Loading...</div>

  return (
    <div className="bg-white rounded-lg shadow border border-gray-200">
      <div className="p-6 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Top Products</h2>
      </div>
      <div className="p-6">
        <div className="space-y-4">
          {products.map((product, index) => (
            <div
              key={product.id}
              className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
            >
              <div className="flex items-center space-x-4">
                <div className="flex items-center justify-center w-8 h-8 bg-indigo-100 text-indigo-600 rounded-full font-bold">
                  {index + 1}
                </div>
                <div>
                  <p className="font-medium text-gray-900">{product.name}</p>
                  <p className="text-sm text-gray-500">
                    {product.sales} sales
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="font-semibold text-gray-900">
                  ₹{product.revenue.toLocaleString()}
                </p>
                <p className="text-sm text-gray-500">Revenue</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
