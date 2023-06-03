package io.github.sampanggabean.myapplication.api

import io.github.sampanggabean.myapplication.api.model.JobScraperApiResponse
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Query

interface ApiService {
    @GET("jobs")
    fun makeRequest(
        @Query("query") query: String?,
        @Query("date_mode") date_mode: String?,
        @Query("date") date: String?,
        @Query("location") location: String?,
        @Query("company") company: String?,
        @Query("page") page: Int?
    ): Call<JobScraperApiResponse>
}