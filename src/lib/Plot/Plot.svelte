<script lang="ts">
    import type { VisualizationSpec, VegaLite } from "svelte-vega";
    import VisSpec from "./VisSpec";
  
    const data = {
      table: [
        { category: "A", amount: 28 },
        { category: "B", amount: 55 },
        { category: "C", amount: 43 },
        { category: "D", amount: 91 },
        { category: "E", amount: 81 },
        { category: "F", amount: 53 },
        { category: "G", amount: 19 },
        { category: "H", amount: 87 },
      ],
    };
  
    // For an example, see https://github.com/vega/svelte-vega/blob/main/packages/storybook/stories/spec1.ts
    const spec: VisualizationSpec = {

    }
  </script>
  
  <VegaLite {data} {spec} />