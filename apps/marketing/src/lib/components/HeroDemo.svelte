<script lang="ts">
	import { theme } from '$lib/stores/theme';
	import { onMount } from 'svelte';

	let mounted = false;
	let analyzing = false;
	let progress = 0;
	let savings = 0;
	let completedSteps = [false, false, false, false, false];
	let showSummary = false;

	// Generate random bill amount between $1,000 and $5,000
	const billAmount = (1000 + Math.random() * 4000).toFixed(2);

	const billTypes = {
		Hospital: {
			name: 'Hospital',
			reasons: ['Emergency Room Visit', 'Outpatient Surgery', 'MRI Scan', 'Physical Therapy']
		},
		Doctor: {
			name: 'Doctor',
			reasons: ['Annual Physical', 'Specialist Consultation', 'Follow-up Visit', 'Preventive Care']
		},
		Labs: {
			name: 'Laboratory',
			reasons: ['Blood Work', 'Diagnostic Tests', 'Pathology Services', 'Medical Screening']
		},
		Dental: {
			name: 'Dental',
			reasons: ['Root Canal', 'Crown Procedure', 'Routine Cleaning', 'Cavity Filling']
		}
	};

	// Generate random bill type and reason
	const billTypes_arr = Object.values(billTypes);
	const randomType = billTypes_arr[Math.floor(Math.random() * billTypes_arr.length)];
	const randomReason = randomType.reasons[Math.floor(Math.random() * randomType.reasons.length)];
	const billNumber = Math.floor(1000 + Math.random() * 9000);

	// Format the bill title
	const billTitle = `${randomType.name} Bill #${billNumber} for ${randomReason} on ${new Date().toLocaleDateString()}`;

	onMount(() => {
		mounted = true;
		startDemo();
	});

	function calculateSavings(total: number) {
		const hospitalServices = total * 0.7;
		const labWork = total * 0.2;
		const medications = total * 0.1;
		// Calculate potential savings (15-20% of total bill)
		return (hospitalServices * 0.15 + labWork * 0.4 + medications * 0.1).toFixed(2);
	}

	function startDemo() {
		analyzing = true;
		progress = 0;
		showSummary = false;
		completedSteps = [false, false, false, false, false];

		const interval = setInterval(() => {
			// Use the same value for both display and progress bar
			const increment = 0.5;
			progress += increment;

			// Update checkmarks at same intervals
			if (progress >= 20) completedSteps[0] = true;
			if (progress >= 40) completedSteps[1] = true;
			if (progress >= 60) completedSteps[2] = true;
			if (progress >= 80) completedSteps[3] = true;
			if (progress >= 100) {
				completedSteps[4] = true;
				clearInterval(interval);
				analyzing = false;
				showSummary = true;
				savings = parseFloat(calculateSavings(parseFloat(billAmount)));
			}
		}, 30); // Slightly slower interval for smoother animation
	}
</script>

<div
	class="rounded-xl border border-violet-100 bg-gradient-to-br from-violet-50/80 via-white/50 to-indigo-50/80 p-6 shadow-lg backdrop-blur-sm"
	role="region"
	aria-label="Bill Analysis Demo"
>
	<div class="mb-4 flex items-center justify-between">
		<h3 class="text-lg font-semibold text-violet-950">AI Bill Analysis</h3>
		<button
			class="rounded-md bg-gradient-to-r from-violet-500 to-violet-600 px-4 py-2 text-sm font-medium text-white shadow-sm transition-all hover:from-violet-600 hover:to-violet-700 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:ring-offset-2"
		>
			Analyze Again
		</button>
	</div>

	<div class="mb-6 rounded-lg bg-white/80 p-4 shadow-sm backdrop-blur-sm">
		<div class="flex items-center justify-between">
			<span class="text-sm text-gray-500">
				{billTitle}
			</span>
			<span class="text-sm font-medium text-gray-600">
				${billAmount}
			</span>
		</div>
		{#if analyzing}
			<div
				class="mt-4"
				role="progressbar"
				aria-valuemin="0"
				aria-valuemax="100"
				aria-valuenow={progress}
			>
				<div class="mb-2 flex justify-between text-xs">
					<span class="text-gray-500">Analyzing bill...</span>
					<span class="text-gray-600">{Math.round(progress)}%</span>
				</div>
				<div class="h-2 overflow-hidden rounded-full bg-violet-100">
					<div
						class="h-2 rounded-full bg-gradient-to-r from-violet-500 to-violet-600 transition-all duration-300"
					/>
				</div>
			</div>
		{:else if savings > 0}
			<div class="mt-4 rounded-md bg-violet-50/80 p-4 shadow-sm backdrop-blur-sm">
				<div class="flex items-center">
					<svg
						class="h-5 w-5 text-violet-500"
						viewBox="0 0 20 20"
						fill="currentColor"
						aria-hidden="true"
					>
						<path
							fill-rule="evenodd"
							d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
							clip-rule="evenodd"
						/>
					</svg>
					<div class="ml-3">
						<p class="text-base font-semibold text-violet-700">
							${savings.toFixed(2)} in Potential Savings
						</p>
						<p class="mt-1 text-sm text-violet-600">
							That's {Math.round((savings / parseFloat(billAmount)) * 100)}% off your total bill
						</p>
					</div>
				</div>
			</div>
		{/if}
	</div>

	<div
		class="space-y-3 lg:grid lg:grid-cols-5 lg:gap-6 lg:space-y-0"
		role="list"
		aria-label="Analysis steps"
	>
		<div class="space-y-3 lg:col-span-3">
			{#each ['Checking for billing errors', 'Verifying insurance coverage', 'Analyzing costs for similar services', 'Finding potential savings', 'Summarizing bill details'] as step, i}
				<div role="listitem">
					<div
						class="flex items-center space-x-2 rounded-lg p-2 text-sm text-gray-600 transition-colors hover:bg-gray-100/50"
					>
						<svg
							class={`h-5 w-5 ${
								completedSteps[i]
									? 'fill-emerald-400 text-emerald-400'
									: 'stroke-gray-300 text-gray-300'
							}`}
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							aria-hidden="true"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
							/>
						</svg>
						<span>{step}</span>
					</div>
				</div>
			{/each}
		</div>

		{#if completedSteps[4]}
			<div
				class={`mt-4 h-full rounded-lg p-6 lg:col-span-2 lg:mt-0 ${'border border-indigo-100 bg-gradient-to-br from-white/70 to-indigo-50/70 shadow-md'}`}
				role="region"
				aria-label="Bill summary"
			>
				<div class="flex h-full flex-col justify-between">
					<div>
						<div class="space-y-3">
							<div>
								<p class="text-sm text-gray-500">Coverage Status</p>
								<p class="text-xs text-emerald-600/90">✓ Service is covered by your plan</p>
								<p class="text-xs text-amber-600">! Pre-authorization may be required</p>
							</div>
						</div>
					</div>

					<div class="mt-6">
						<p class="text-sm text-gray-500">Cost Breakdown</p>
						<div class="mt-1 space-y-1 text-xs">
							<div class="flex justify-between">
								<span class="text-gray-500">Original Bill</span>
								<span class="text-gray-600">${billAmount}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-emerald-600/90">Potential Savings</span>
								<span class="text-emerald-600/90">-${savings.toFixed(2)}</span>
							</div>
							<div class="flex justify-between border-t pt-1 font-medium">
								<span class="text-gray-500">Estimated Final</span>
								<span class="text-gray-600">${(parseFloat(billAmount) - savings).toFixed(2)}</span>
							</div>
						</div>
					</div>
				</div>
			</div>
		{/if}
	</div>
</div>
