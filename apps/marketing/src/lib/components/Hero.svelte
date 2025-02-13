<script lang="ts">
	import { theme } from '$lib/stores/theme';
</script>

<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
	<div class="flex min-h-[600px] items-center py-12">
		<div class="grid gap-12 lg:grid-cols-2">
			<div>
				<h1 class="text-5xl font-bold leading-tight text-white lg:text-6xl">
					Your Health Data,<br />
					<span class="text-[#94A3B8]">Your Rules</span>
				</h1>
				<p class="mt-6 text-lg leading-relaxed text-[#94A3B8]">
					Cleanbill consolidates your medical records into one easy-to-understand timeline that you
					own. Take control of your health journey, manage who can access your health data, and have
					better conversations with your doctor.
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
			<!-- Uncomment when you have the image -->
			<!-- <div class="relative">
				<img
					src="/dashboard.png"
					alt="Cleanbill Dashboard"
					class="w-full rounded-lg object-cover shadow-xl"
				/>
			</div> -->
		</div>
	</div>
</div>
