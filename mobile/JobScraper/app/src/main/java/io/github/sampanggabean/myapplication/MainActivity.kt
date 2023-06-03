package io.github.sampanggabean.myapplication

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.Menu
import androidx.activity.viewModels
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import io.github.sampanggabean.myapplication.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    private lateinit var menu: Menu

    private val binding: ActivityMainBinding by lazy {
        ActivityMainBinding.inflate(layoutInflater)
    }

    private val viewModel: MainViewModel by viewModels {
        ViewModelProvider.NewInstanceFactory()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)
        setSupportActionBar(binding.toolbar)

        binding.buttonFilter.setOnClickListener {
            val itemListDialogFragment = ItemListDialogFragment()
            itemListDialogFragment.show(supportFragmentManager, null)
        }

        viewModel.jobs.observe(this) {jobs ->
            binding.recyclerView.swapAdapter(JobAdapter(jobs.filterNotNull()), true)
        }

        binding.recyclerView.layoutManager = LinearLayoutManager(this)
    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.page, menu)
        this.menu = menu as Menu
        menu.findItem(R.id.next_page).setOnMenuItemClickListener {
            viewModel.nextPage()
            true
        }
        menu.findItem(R.id.prev_page).setOnMenuItemClickListener {
            viewModel.prevPage()
            true
        }

        viewModel.page.observe(this) {pageNumber ->
            menu.findItem(R.id.page_number).title = (pageNumber ?: 1) .toString()
        }
        return true
    }
}