import type { Category } from '../types/api'

export const CATEGORY_META: Record<Category, { label: string; color: string; chartColor: string; emoji: string }> = {
    food: { label: 'Food', color: 'bg-orange-100 text-orange-700', chartColor: '#f97316', emoji: '🍔' },
    transport: { label: 'Transport', color: 'bg-blue-100 text-blue-700', chartColor: '#3b82f6', emoji: '🚌' },
    housing: { label: 'Housing', color: 'bg-purple-100 text-purple-700', chartColor: '#8b5cf6', emoji: '🏠' },
    health: { label: 'Health', color: 'bg-red-100 text-red-700', chartColor: '#ef4444', emoji: '💊' },
    entertainment: { label: 'Entertainment', color: 'bg-pink-100 text-pink-700', chartColor: '#ec4899', emoji: '🎬' },
    education: { label: 'Education', color: 'bg-green-100 text-green-700', chartColor: '#22c55e', emoji: '📚' },
    clothing: { label: 'Clothing', color: 'bg-yellow-100 text-yellow-700', chartColor: '#eab308', emoji: '👕' },
    other: { label: 'Other', color: 'bg-gray-100 text-gray-700', chartColor: '#6b7280', emoji: '📦' },
}