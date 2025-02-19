import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
    console.log("Middleware executing for:", request.nextUrl.pathname)

    // During development, let's allow access to all routes
    if (process.env.NODE_ENV === 'development') {
        return NextResponse.next()
    }

    let response = NextResponse.next({
        request: {
            headers: request.headers,
        },
    })

    try {
        const supabase = createServerClient(
            process.env.NEXT_PUBLIC_SUPABASE_URL!,
            process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
            {
                cookies: {
                    get(name: string) {
                        return request.cookies.get(name)?.value
                    },
                    set(name: string, value: string, options: CookieOptions) {
                        response.cookies.set({
                            name,
                            value,
                            ...options,
                        })
                    },
                    remove(name: string, options: CookieOptions) {
                        response.cookies.set({
                            name,
                            value: '',
                            ...options,
                        })
                    },
                },
            }
        )

        const { data: { session }, error } = await supabase.auth.getSession()
        console.log("Middleware session check:", { session, error }) // Debug log

        if (error) {
            console.error('Session error:', error)
            // During development, let's just log the error and continue
            return response
        }

        // If user is not signed in and trying to access protected routes
        if (!session) {
            if (request.nextUrl.pathname !== '/auth') {
                return NextResponse.redirect(new URL('/auth', request.url))
            }
        }

        // If user is signed in
        if (session) {
            const finishedWelcomeFlow = request.cookies.get("finishedWelcomeFlow")?.value === "true"
            const referer = request.headers.get("referer") || ""
            const isFromDashboard = referer.includes("/dashboard")

            // Handle auth page access
            if (request.nextUrl.pathname === '/auth') {
                return NextResponse.redirect(new URL(finishedWelcomeFlow ? '/dashboard' : '/welcome', request.url))
            }

            // Handle root path
            if (request.nextUrl.pathname === '/') {
                return NextResponse.redirect(new URL(finishedWelcomeFlow ? '/dashboard' : '/welcome', request.url))
            }

            // Only redirect /welcome to /dashboard if welcome flow is completed AND not coming from dashboard
            if (request.nextUrl.pathname === '/welcome' && finishedWelcomeFlow && !isFromDashboard) {
                return NextResponse.redirect(new URL('/dashboard', request.url))
            }
        }

        return response
    } catch (error) {
        console.error("Middleware error:", error)
        // During development, let's just log the error and continue
        return response
    }
}

export const config = {
    matcher: [
        '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
    ],
} 