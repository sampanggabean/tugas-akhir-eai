package io.github.sampanggabean.myapplication

import android.os.Bundle
import com.google.android.material.bottomsheet.BottomSheetDialogFragment
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.activityViewModels
import androidx.lifecycle.ViewModelProvider
import io.github.sampanggabean.myapplication.databinding.FragmentItemListDialogListDialogBinding

/**
 *
 * A fragment that shows a list of items as a modal bottom sheet.
 *
 * You can show this modal bottom sheet from your activity like this:
 * <pre>
 *    ItemListDialogFragment.newInstance(30).show(supportFragmentManager, "dialog")
 * </pre>
 */
class ItemListDialogFragment : BottomSheetDialogFragment() {

    private var _binding: FragmentItemListDialogListDialogBinding? = null
    private val binding get() = _binding as FragmentItemListDialogListDialogBinding
    private val viewModel: MainViewModel by activityViewModels {
        ViewModelProvider.NewInstanceFactory()
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {

        _binding = FragmentItemListDialogListDialogBinding.inflate(inflater, container, false)
        return binding.root

    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        binding.switchDateMode.setOnCheckedChangeListener {_, isChecked ->
            binding.switchDateMode.text = if (isChecked) "After" else "Before"
        }
        binding.buttonSubmit.setOnClickListener {
            val date_mode = if (binding.switchDateMode.isChecked) "after" else "before"
            val date = "${binding.datePicker.year}-${binding.datePicker.month}-${binding.datePicker.dayOfMonth}"
            val location = binding.editTextLocation.text.toString()
            val company = binding.editTextCompany.text.toString()
            val page = 1
            val strBuilder = StringBuilder()
            if (binding.checkBoxData.isChecked) {
                strBuilder.append("Data,")
            }
            if (binding.checkBoxNetwork.isChecked) {
                strBuilder.append("Network,")
            }
            if (binding.checkBoxCyberSecurity.isChecked) {
                strBuilder.append("Cyber Security,")
            }
            if (binding.checkBoxProgrammer.isChecked) {
                strBuilder.append("Programmer,")
            }
            if (strBuilder.isNotBlank()) {
                strBuilder.deleteCharAt(strBuilder.length - 1)
            }
            val query = strBuilder.toString()
            viewModel.makeRequest(query, date_mode, date, location, company, page)
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}