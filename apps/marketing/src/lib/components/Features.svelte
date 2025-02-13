<script lang="ts">
	import { theme } from '$lib/stores/theme';

	const features = [
		{
			icon: 'lock',
			title: 'Smart Bill Analysis',
			description:
				'Our AI technology scans your medical bills for errors and overcharges, helping you avoid unnecessary expenses and identify potential savings.'
		},
		{
			icon: 'share',
			title: 'Insurance Benefit Decoder',
			description:
				'Understand your insurance benefits in plain English. We translate complex EOBs into clear, actionable information you can use.'
		},
		{
			icon: 'monitor',
			title: 'Cost Management Assistant',
			description:
				'Get personalized insights and recommendations to help you navigate healthcare expenses and make informed financial decisions.'
		}
	];
</script>

<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
	<section class="py-24">
		<div class="text-center">
			<h2 class={`text-4xl font-bold ${$theme ? 'text-white' : 'text-[#1F2937]'}`}>
				Simplify Your Healthcare Bills
			</h2>
			<p class={`mx-auto mt-4 max-w-3xl text-xl ${$theme ? 'text-[#94A3B8]' : 'text-[#6B7280]'}`}>
				Let AI help you understand and manage your medical expenses with confidence
			</p>
		</div>
		<div class="mt-20 grid gap-8 lg:grid-cols-3">
			{#each features as feature}
				<div
					class={`rounded-2xl border p-8 ${
						$theme ? 'border-gray-700 bg-[#1F2937]' : 'border-gray-200 bg-white'
					}`}
				>
					<div class="mb-6 inline-block rounded-lg bg-[#3B82F6] p-3">
						{#if feature.icon === 'lock'}
							<svg class="h-6 w-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
								/>
							</svg>
						{:else if feature.icon === 'share'}
							<svg class="h-6 w-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"
								/>
							</svg>
						{:else if feature.icon === 'monitor'}
							<svg class="h-6 w-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
								/>
							</svg>
						{/if}
					</div>
					<h3 class={`text-xl font-semibold ${$theme ? 'text-white' : 'text-[#1F2937]'}`}>
						{feature.title}
					</h3>
					<p class={`mt-2 ${$theme ? 'text-[#94A3B8]' : 'text-[#6B7280]'}`}>
						{feature.description}
					</p>
				</div>
			{/each}
		</div>
	</section>
</div>
