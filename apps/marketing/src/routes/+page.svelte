<script lang="ts">
	import Content from '$lib/components/Content.svelte';
	import Hero from '$lib/components/Hero.svelte';
	import Features from '$lib/components/Features.svelte';
	import Details from '$lib/components/Details.svelte';
	import Action from '$lib/components/Action.svelte';
	import { theme } from '$lib/stores/theme';
</script>

<div class="w-full bg-[rgb(29,63,172)]">
	<Content>
		<Hero />
	</Content>
</div>

<div class={`w-full ${$theme ? 'bg-black' : 'bg-white'}`}>
	<Content>
		<Features />
	</Content>
</div>

<div class={`w-full ${$theme ? 'bg-[#1E293B]' : 'bg-[#F9FAFB]'}`}>
	<Content>
		<Details />
	</Content>
</div>

<div class="w-full bg-[rgb(29,63,172)]">
	<Content>
		<Action />
	</Content>
</div>
