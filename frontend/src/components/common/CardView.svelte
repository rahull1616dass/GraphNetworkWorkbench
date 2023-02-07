<script lang="ts">


</script>


<div class="CardView">

    <slot class = "header"> </slot>
    <slot class = "body"> </slot>
    <slot class = "footer"> </slot>

</div>

<style lang="scss">

    .CardView {
        position: center;
        width: 35%;
        margin-left: 5%;
        margin-top: 1%;
        margin-bottom: 3%;
        border-radius: 15px;
        box-shadow: 2px 3px 4px rgba(0,0,0,0.2);
        background-color: whitesmoke;
    }

</style>