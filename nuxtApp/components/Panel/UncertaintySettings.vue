<template>
  <box title="Uncertainty Settings">
    <div class="input-ele-group first">
      <label class="bold">Uncertainty index system</label>
    </div>
    <table>
      <tr v-for="(item, i) in uncertaintyIndex">
        <td width="240px">U{{ i }}: {{ item.name }}</td>
        <td width="300px">
          weight:
          <input
            type="text"
            style="width: 30px; text-align: center"
            :value="item.weight"
          />
        </td>
      </tr>
    </table>
    <div class="control-content">
      <div class="input-ele-group first">
        <label class="bold">Uncertainty levels</label>
      </div>
      <ul>
        <li v-for="(item, i) in uncertaintyLevels" :key="i">
          Level {{ i + 1 }}:
          <i v-for="j in i + 1" class="el-icon-star-on"></i>
          {{ item }}
        </li>
      </ul>
    </div>
  </box>
</template>

<script>
import box from './box.vue'

export default {
  name: 'UncertaintySettings',
  components: {
    box,
  },
  data() {
    return {
      uncertaintyIndex: [
        {
          name: 'Inconsistency',
          weight: 1,
        },
        {
          name: 'Credibility',
          weight: 1,
        },
        {
          name: 'Precision',
          weight: 1,
        },
        {
          name: 'Data completeness',
          weight: 1,
        },
      ],
      uncertaintyLevels: ['low', 'guarded', 'elevated', 'high', 'severe'],
    }
  },
}
</script>

<style></style>
