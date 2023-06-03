package io.github.sampanggabean.myapplication

import android.util.Log
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import io.github.sampanggabean.myapplication.api.model.ApiConfig
import io.github.sampanggabean.myapplication.api.model.JobScraperApiResponse
import io.github.sampanggabean.myapplication.api.model.ResultsItem
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class MainViewModel : ViewModel() {
    private val apiService = ApiConfig.getApiService()

    private val _jobs = MutableLiveData<List<ResultsItem?>>()
    val jobs: LiveData<List<ResultsItem?>> = _jobs

    private val _query = MutableLiveData<String?>()
    private val _datemode = MutableLiveData<String?>()
    private val _date = MutableLiveData<String?>()
    private val _location = MutableLiveData<String?>()
    private val _company = MutableLiveData<String?>()
    private val _page = MutableLiveData<Int>(1)
    val page: LiveData<Int?> = _page

    init {
        makeRequest(null, null, null, null, null, 1)
    }

    fun makeRequest(
        query: String?,
        date_mode: String?,
        date: String?,
        location: String?,
        company: String?,
        page: Int?
    ) {
        _query.value = query
        _datemode.value = date_mode
        _date.value = date
        _location.value = location
        _company.value = company
        _page.value = page
        apiService.makeRequest(query, date_mode, date, location, company, page).enqueue(object : Callback<JobScraperApiResponse> {
            override fun onResponse(
                call: Call<JobScraperApiResponse>,
                response: Response<JobScraperApiResponse>
            ) {
                val body = response.body()
                val returnedJobs = body?.results
                _jobs.value = returnedJobs ?: listOf()
            }

            override fun onFailure(call: Call<JobScraperApiResponse>, t: Throwable) {
                Log.d("MainViewModel", "FAILED")
            }

        })
    }

    fun nextPage() {
        val page = _page.value?.plus(1)
        _page.value = page
        makeRequest(_query.value, _datemode.value, _date.value, _location.value, _company.value, page)
    }

    fun prevPage() {
        val page = if(_page.value == null || _page.value == 1) _page.value else _page.value?.minus(1)
        _page.value = page
        makeRequest(_query.value, _datemode.value, _date.value, _location.value, _company.value, page)
    }
}