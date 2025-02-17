import { createClientComponentClient } from '@supabase/auth-helpers-nextjs'

// Create a single Supabase client for the browser
export const supabase = createClientComponentClient() 