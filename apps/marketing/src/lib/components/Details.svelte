<script lang="ts">
	import { theme } from '$lib/stores/theme';

	const details = [
		{
			icon: 'check',
			title: 'Better Care Coordination',
			description:
				'Share accurate, complete records with any provider instantly. No more repeating tests or missing critical information.'
		},
		{
			icon: 'bolt',
			title: 'Personalized Insights',
			description:
				'Use AI models of your choice to analyze your complete health history and get personalized recommendations.'
		},
		{
			icon: 'fingerprint',
			title: 'Privacy & Control',
			description:
				'Choose who sees what and for how long. Revoke access anytime. Your sensitive health information stays under your control.'
		},
		{
			icon: 'clock',
			title: 'Emergency Access',
			description:
				'Grant immediate access to your records in emergencies. Critical information available when seconds count.'
		},
		{
			icon: 'chart',
			title: 'Research Participation',
			description:
				'Choose to contribute your data to medical research. Help advance healthcare while maintaining your privacy.'
		},
		{
			icon: 'dollar',
			title: 'Cost Savings',
			description:
				'Avoid duplicate tests and procedures. Share previous results with new providers to save time and money.'
		}
	];
</script>

<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
	<section class="py-24">
		<div class="text-center">
			<h2 class={`text-4xl font-bold ${$theme ? 'text-white' : 'text-[#1F2937]'}`}>
				Why Own Your Health Records?
			</h2>
			<p class={`mx-auto mt-4 max-w-3xl text-xl ${$theme ? 'text-[#94A3B8]' : 'text-[#6B7280]'}`}>
				Your health records are more than just documents – they're the key to better healthcare
			</p>
		</div>
		<div class="mt-20 grid gap-8 md:grid-cols-2 lg:grid-cols-3">
			{#each details as detail}
				<div class={`rounded-2xl p-8 ${$theme ? 'bg-[#0F172A]' : 'bg-white'}`}>
					<div class="mb-6 inline-block rounded-lg bg-[#3B82F6] p-3">
						{#if detail.icon === 'check'}
							<svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M5 13l4 4L19 7"
								/>
							</svg>
						{:else if detail.icon === 'bolt'}
							<svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M13 10V3L4 14h7v7l9-11h-7z"
								/>
							</svg>
						{:else if detail.icon === 'fingerprint'}
							<svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 008 4.07M3 15.364c.64-1.319 1-2.8 1-4.364 0-1.457.39-2.823 1.07-4"
								/>
							</svg>
						{:else if detail.icon === 'clock'}
							<svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
								/>
							</svg>
						{:else if detail.icon === 'chart'}
							<svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
								/>
							</svg>
						{:else if detail.icon === 'dollar'}
							<svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
								/>
							</svg>
						{/if}
					</div>
					<h3 class={`text-xl font-semibold ${$theme ? 'text-white' : 'text-[#1F2937]'}`}>
						{detail.title}
					</h3>
					<p class={`mt-2 ${$theme ? 'text-[#94A3B8]' : 'text-[#6B7280]'}`}>
						{detail.description}
					</p>
				</div>
			{/each}
		</div>
	</section>
</div>
