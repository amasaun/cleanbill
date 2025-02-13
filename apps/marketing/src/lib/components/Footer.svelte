<script lang="ts">
	import { theme } from '$lib/stores/theme';
</script>

<div class={`w-full ${$theme ? 'bg-black' : 'bg-white'}`}>
	<div class="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
		<div class="flex flex-col items-center justify-between md:flex-row">
			<div class="flex items-center space-x-2">
				<img
					src={$theme ? '/icon-white.svg' : '/icon-blue.svg'}
					alt="Cleanbill Icon"
					class="h-8 w-8"
				/>
				<img src={$theme ? '/logo-white.svg' : '/logo-blue.svg'} alt="Cleanbill" class="h-8" />
			</div>
			<div class="mt-4 text-center md:mt-0">
				<p class={`text-sm ${$theme ? 'text-gray-400' : 'text-gray-600'}`}>
					© {new Date().getFullYear()} Cleanbill. All rights reserved.
				</p>
			</div>
			<div class="mt-4 flex space-x-6 md:mt-0">
				<a
					href="/privacy"
					class={`text-sm ${$theme ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-black'}`}
				>
					Privacy Policy
				</a>
				<a
					href="/terms"
					class={`text-sm ${$theme ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-black'}`}
				>
					Terms of Service
				</a>
			</div>
		</div>
	</div>
</div>
