'use client'

import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
import Dashboard from './dashboard/page'

export default function Home() {
  const router = useRouter()

  useEffect(() => {
    router.push('/dashboard')
  }, [router])

  return null
}
