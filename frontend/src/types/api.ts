export type Category =
    | "food"
    | "transport"
    | "housing"
    | "health"
    | "entertainment"
    | "education"
    | "clothing"
    | "other";

export interface User {
    id: string;
    email: string;
    created_at: string;
}

export interface AuthResponse {
    user: User;
    access_token: string;
}

export interface ApiError {
    error: {
        code: string;
        message: string;
    };
}

export interface Expense {
    id: string;
    user_id: string;
    amount: string;
    category: Category;
    description?: string;
    date: string;
    created_at: string;
}

export interface ExpenseCreate {
    amount: string;
    category: Category;
    description?: string;
    date: string;
}

export interface ExpenseSummary {
    total: string;
    by_category: Record<Category, string>;
    by_day: { date: string; total: string }[];
}