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
			progress += 0.5;

			if (progress >= 20) completedSteps[0] = true;
			if (progress >= 40) completedSteps[1] = true;
			if (progress >= 60) completedSteps[2] = true;
			if (progress >= 80) completedSteps[3] = true;
			if (progress >= 100) {
				progress = 100; // Ensure we stop exactly at 100
				completedSteps[4] = true;
				clearInterval(interval);
				analyzing = false;
				showSummary = true;
				savings = parseFloat(calculateSavings(parseFloat(billAmount)));
			}
		}, 30);
	}
</script>

<!-- Main container - responsive height -->
<div
	class="relative h-auto min-h-[560px] rounded-2xl bg-gradient-to-br from-slate-50 to-slate-100/80 p-4 shadow-lg backdrop-blur-sm sm:h-[560px]"
>
	<!-- Header - minimal margins -->
	<div class="mb-1.5 flex items-center justify-between">
		{#if completedSteps[4]}
			<div>
				<h3 class="text-lg font-semibold text-slate-800">Bill Analysis Complete</h3>
				<p class="mt-0.5 text-sm text-slate-500">Due in 30 days</p>
			</div>
		{:else}
			<h3 class="text-lg font-semibold text-slate-800">Bill Analysis</h3>
		{/if}
		<button
			on:click={startDemo}
			class="rounded-full bg-violet-600 px-4 py-1.5 text-sm font-medium text-white shadow-sm transition-all hover:bg-violet-700"
		>
			Analyze Again
		</button>
	</div>

	<!-- Only show bill info card during analysis -->
	{#if !completedSteps[4]}
		<div class="mb-3 rounded-xl bg-white p-3 shadow-sm">
			<!-- Bill header -->
			<div class="flex items-center justify-between">
				<div class="flex-1">
					<p class="text-sm font-medium text-slate-800">{billTitle}</p>
					<p class="mt-0.5 text-xs text-slate-500">Due in 30 days</p>
				</div>
				<p class="ml-4 text-lg font-semibold text-slate-800">${billAmount}</p>
			</div>

			<!-- Analysis progress -->
			<div class="mt-3">
				{#if analyzing}
					<div
						class="rounded-lg bg-violet-50 p-3"
						role="progressbar"
						aria-valuemin="0"
						aria-valuemax="100"
						aria-valuenow={progress}
					>
						<div class="flex items-start justify-between">
							<div class="flex flex-1 items-start gap-3">
								<div class="rounded-full bg-violet-100 p-2">
									<svg
										class="h-5 w-5 animate-pulse text-violet-600"
										viewBox="0 0 24 24"
										fill="currentColor"
										stroke="none"
									>
										<!-- Large star -->
										<path d="M12 4L14.4 11.6L22 14L14.4 16.4L12 24L9.6 16.4L2 14L9.6 11.6L12 4Z" />

										<!-- Small star - moved higher and more to the right -->
										<path d="M18 1L19 4L22 5L19 6L18 9L17 6L14 5L17 4L18 1Z" />
									</svg>
								</div>
								<div class="flex-1">
									<p class="font-semibold text-violet-900">Analyzing Your Bill</p>
									<div class="mt-2 w-full">
										<div class="h-2.5 overflow-hidden rounded-full bg-violet-100">
											<div
												class="h-full rounded-full bg-violet-600 transition-all duration-300"
												style:width="{progress}%"
											/>
										</div>
									</div>
								</div>
							</div>

							<p class="ml-4 text-sm font-medium text-violet-700">
								{progress.toFixed(1)}%
							</p>
						</div>
					</div>
				{/if}
			</div>
		</div>
	{/if}

	<!-- Summary section -->
	<div class="grid h-auto gap-2 max-sm:h-[600px] sm:h-[490px]">
		{#if completedSteps[4]}
			<div class="mb-5 rounded-xl bg-white p-3 shadow-sm">
				<!-- Bill Widget - Added at Top -->
				<div class="mb-3 flex items-center justify-between">
					<div>
						<p class="text-sm font-medium text-slate-800">{billTitle}</p>
						<p class="mt-0.5 text-xs text-slate-500">Due in 30 days</p>
					</div>
					<p class="ml-4 text-lg font-semibold text-slate-800">${billAmount}</p>
				</div>

				<!-- Total Savings Summary -->
				<div class="mb-2 rounded-lg bg-violet-50 p-3">
					<h4 class="mb-2 text-lg font-medium text-violet-900">We Found Savings! 🎉</h4>
					<p class="text-2xl font-semibold text-violet-900">
						${savings.toFixed(2)} Potential Savings Found
					</p>
					<p class="mt-1 text-sm text-violet-700">
						We found ways to reduce your bill by {Math.round(
							(savings / parseFloat(billAmount)) * 100
						)}%
					</p>

					<div class="mt-3 space-y-2">
						<div class="flex items-start gap-2">
							<div class="mt-1 rounded-full bg-violet-100 p-1">
								<svg class="h-3 w-3 text-violet-600" viewBox="0 0 20 20" fill="currentColor">
									<path
										d="M10.75 2.75a.75.75 0 00-1.5 0v8.614L6.295 8.235a.75.75 0 10-1.09 1.03l4.25 4.5a.75.75 0 001.09 0l4.25-4.5a.75.75 0 00-1.09-1.03l-2.955 3.129V2.75z"
									/>
								</svg>
							</div>
							<div>
								<p class="font-medium text-violet-900">Lower Regional Rate Available</p>
								<p class="text-violet-700">Save ${(parseFloat(billAmount) * 0.15).toFixed(2)}</p>
							</div>
						</div>
						<div class="flex items-start gap-2">
							<div class="mt-1 rounded-full bg-violet-100 p-1">
								<svg class="h-3 w-3 text-violet-600" viewBox="0 0 20 20" fill="currentColor">
									<path
										d="M10.75 2.75a.75.75 0 00-1.5 0v8.614L6.295 8.235a.75.75 0 10-1.09 1.03l4.25 4.5a.75.75 0 001.09 0l4.25-4.5a.75.75 0 00-1.09-1.03l-2.955 3.129V2.75z"
									/>
								</svg>
							</div>
							<div>
								<p class="font-medium text-violet-900">Additional Network Discount</p>
								<p class="text-violet-700">Save ${(parseFloat(billAmount) * 0.1).toFixed(2)}</p>
							</div>
						</div>
					</div>
				</div>

				<!-- Important Information -->
				<div class="rounded-lg border border-amber-100 bg-amber-50 p-3">
					<h4 class="mb-2 text-base font-medium text-amber-800">Important Information</h4>
					<div class="grid gap-3 sm:grid-cols-2">
						<div class="flex items-center gap-2">
							<div class="rounded-full bg-emerald-100 p-1.5">
								<svg class="h-3 w-3 text-emerald-600" viewBox="0 0 20 20" fill="currentColor">
									<path
										d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
									/>
								</svg>
							</div>
							<span class="text-sm text-amber-800">Service is covered by your plan</span>
						</div>
						<div class="flex items-center gap-2">
							<div class="rounded-full bg-amber-200 p-1.5">
								<svg class="h-3 w-3 text-amber-700" viewBox="0 0 20 20" fill="currentColor">
									<path
										d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495z"
									/>
								</svg>
							</div>
							<span class="text-sm text-amber-800">Pre-authorization required</span>
						</div>
						<div class="flex items-center gap-2">
							<div class="rounded-full bg-blue-100 p-1.5">
								<svg class="h-3 w-3 text-blue-600" viewBox="0 0 20 20" fill="currentColor">
									<path
										d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6z"
									/>
								</svg>
							</div>
							<span class="text-sm text-amber-800">Deductible: $2,850 remaining</span>
						</div>
						<div class="flex items-center gap-2">
							<div class="rounded-full bg-violet-100 p-1.5">
								<svg class="h-3 w-3 text-violet-600" viewBox="0 0 20 20" fill="currentColor">
									<path
										d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6z"
									/>
								</svg>
							</div>
							<span class="text-sm text-amber-800">Plan Year: 80% complete</span>
						</div>
					</div>
				</div>
			</div>
		{:else}
			<!-- Analysis steps - adjust spacing -->
			<div class="space-y-1.5">
				{#each ['Checking for billing errors', 'Verifying insurance coverage', 'Analyzing costs for similar services', 'Finding potential savings', 'Summarizing bill details'] as step, i}
					<div
						class="flex items-center gap-3 rounded-lg px-3 py-2 transition-colors hover:bg-white/50"
					>
						<div class={`rounded-full p-1 ${completedSteps[i] ? 'bg-violet-100' : 'bg-slate-100'}`}>
							<svg
								class={`h-4 w-4 ${completedSteps[i] ? 'text-violet-600' : 'text-slate-400'}`}
								viewBox="0 0 20 20"
								fill="currentColor"
							>
								<path
									d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
								/>
							</svg>
						</div>
						<span class={`text-sm ${completedSteps[i] ? 'text-slate-800' : 'text-slate-500'}`}>
							{step}
						</span>
					</div>
				{/each}
			</div>
		{/if}
	</div>
</div>
