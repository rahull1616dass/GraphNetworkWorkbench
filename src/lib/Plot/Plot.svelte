<script lang="ts">
    /*

    import { Vega } from "svelte-vega"

  
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
    const spec = VisSpec
    */
    import type { VisualizationSpec } from "svelte-vega"
    import  MiserablesData  from "../../data/VisSpec"
    import {default as vegaEmbed} from 'vega-embed';
    var spec = "https://vega.github.io/vega/examples/force-directed-layout.vg.json";

    vegaEmbed("#viz", MiserablesData, { actions: false }).catch(error => console.log(error) );

  </script>
  
  <!--
  <Vega {data} {spec} />
  -->
  <div id="viz"></div>

<p>Hello Plotsdfas</p>