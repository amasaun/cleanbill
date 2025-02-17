import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(req: NextRequest) {
    const res = NextResponse.next()
    const supabase = createMiddlewareClient({
        req,
        res,
    })

    const { data: { session }, error } = await supabase.auth.getSession()

    if (error) {
        console.error('Session error:', error)
        return NextResponse.redirect(new URL('/auth', req.url))
    }

    // If user is not signed in and trying to access protected routes
    if (!session) {
        if (req.nextUrl.pathname !== '/auth') {
            return NextResponse.redirect(new URL('/auth', req.url))
        }
    }

    // If user is signed in
    if (session) {
        const finishedWelcomeFlow = req.cookies.get("finishedWelcomeFlow")?.value === "true"
        const referer = req.headers.get("referer") || ""
        const isFromDashboard = referer.includes("/dashboard")

        // Handle auth page access
        if (req.nextUrl.pathname === '/auth') {
            return NextResponse.redirect(new URL(finishedWelcomeFlow ? '/dashboard' : '/welcome', req.url))
        }

        // Handle root path
        if (req.nextUrl.pathname === '/') {
            return NextResponse.redirect(new URL(finishedWelcomeFlow ? '/dashboard' : '/welcome', req.url))
        }

        // Only redirect /welcome to /dashboard if welcome flow is completed AND not coming from dashboard
        if (req.nextUrl.pathname === '/welcome' && finishedWelcomeFlow && !isFromDashboard) {
            return NextResponse.redirect(new URL('/dashboard', req.url))
        }
    }

    return res
}

export const config = {
    matcher: ['/', '/auth', '/welcome', '/dashboard']
} 