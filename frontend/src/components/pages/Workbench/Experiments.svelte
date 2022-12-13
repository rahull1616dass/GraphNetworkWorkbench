<script lang="ts">
  import lockIcon from "../../../assets/lock.svg"
  import rightArrowIcon from "../../../assets/arrow_right.svg"
  import { networksList, selectedNetworkIndex } from "../../../stores";
</script>

<div class="train_box">

</div>


<style lang="scss">
    .train_box {
        width: 100%;
        height: 100%;
        background-color: #f5f5f5;
        border-radius: 5px;
        padding: 10px;
        margin: 10px;
        cursor: pointer;
        transition: background-color 0.2s ease-in-out;
        margin: 10px;
        &.selected {
            background-color: #e5e5e5;
        }
    }
</style>
