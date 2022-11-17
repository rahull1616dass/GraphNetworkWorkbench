<script lang="ts">
    import  MiserablesData  from "../../data/VisSpec"
    import {default as vegaEmbed} from 'vega-embed';
    // Refer https://www.koderhq.com/tutorial/svelte/json-storage/
    vegaEmbed("#viz", MiserablesData, { actions: false }).catch(error => console.log(error) );

  </script>
  
  <div id="viz"></div>

<p>Hello Plotsdfas</p>