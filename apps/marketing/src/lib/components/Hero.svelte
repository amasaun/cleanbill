<script lang="ts">
	import { theme } from '$lib/stores/theme';
	import HeroDemo from './HeroDemo.svelte';
</script>

<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
	<div class="flex min-h-[600px] items-center py-12">
		<div class="grid gap-12 lg:grid-cols-2">
			<div>
				<h1 class="text-5xl font-bold leading-tight text-white lg:text-6xl">
					Understand Your<br />
					<span class="text-[#94A3B8]">Healthcare Costs</span>
				</h1>
				<p class="mt-6 text-lg leading-relaxed text-[#94A3B8]">
					Cleanbill uses AI to securely and privately decode your medical bills and insurance
					benefits. We make healthcare expenses simple to understand, identify potential savings,
					and help you take control of your healthcare costs.
				</p>
				<div class="mt-8">
					<a
						href="/join-waitlist"
						class="inline-block rounded-md bg-[#6366F1] px-6 py-3 text-base font-medium text-white hover:bg-opacity-90"
					>
						Join the Waitlist
					</a>
				</div>
			</div>
			<div class="relative">
				<HeroDemo />
			</div>
		</div>
	</div>
</div>
