package io.github.sampanggabean.myapplication

import android.content.Intent
import android.net.Uri
import android.util.Log
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import io.github.sampanggabean.myapplication.api.model.ResultsItem
import io.github.sampanggabean.myapplication.databinding.JobItemBinding

class JobAdapter(private val jobs: List<ResultsItem>) : RecyclerView.Adapter<JobAdapter.JobViewHolder>() {
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): JobViewHolder {
        val binding = JobItemBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return JobViewHolder(binding)
    }

    override fun onBindViewHolder(holder: JobViewHolder, position: Int) {
        holder.bind(jobs[position])
    }

    override fun getItemCount(): Int {
        return jobs.size
    }

    class JobViewHolder(private val binding: JobItemBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(job: ResultsItem) {
            try {
                binding.imageViewSource.setImageResource(when(job.source) {
                    "linkedin.com/jobs" -> R.drawable.linkedin
                    "jobstreet.co.id" -> R.drawable.jobstreet
                    "kalibrr.com" -> R.drawable.kalibrr
                    else -> R.drawable.karir
                })
                val context = binding.root.context
                binding.textViewPosition.text = job.position
                binding.textViewCompany.text = context.resources.getString(R.string.company_text, job.company)
                binding.textViewLocation.text = job.location
                binding.textViewCreatedAt.text = context.resources.getString(R.string.created_at, job.createdAt)
                binding.buttonUrl.setOnClickListener {
                    context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(job.url)))
                }
            } catch (e: Exception) {
                Log.e("Job Adapter", "Error processing a job")
                Log.e("Job Adapter", e.message.toString())
            }
        }
    }

}