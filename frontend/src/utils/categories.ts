import type { Category } from '../types/api'

export const CATEGORY_META: Record<Category, { label: string; color: string; emoji: string }> = {
    food: { label: 'Food', color: 'bg-orange-100 text-orange-700', emoji: '🍔' },
    transport: { label: 'Transport', color: 'bg-blue-100 text-blue-700', emoji: '🚌' },
    housing: { label: 'Housing', color: 'bg-purple-100 text-purple-700', emoji: '🏠' },
    health: { label: 'Health', color: 'bg-red-100 text-red-700', emoji: '💊' },
    entertainment: { label: 'Entertainment', color: 'bg-pink-100 text-pink-700', emoji: '🎬' },
    education: { label: 'Education', color: 'bg-green-100 text-green-700', emoji: '📚' },
    clothing: { label: 'Clothing', color: 'bg-yellow-100 text-yellow-700', emoji: '👕' },
    other: { label: 'Other', color: 'bg-gray-100 text-gray-700', emoji: '📦' },
}