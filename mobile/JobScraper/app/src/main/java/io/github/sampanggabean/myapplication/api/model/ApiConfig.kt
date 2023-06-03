package io.github.sampanggabean.myapplication.api.model

import io.github.sampanggabean.myapplication.api.ApiService
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object ApiConfig {
    fun getApiService(): ApiService {
        val gsonConverterFactory = GsonConverterFactory.create()
        val client = OkHttpClient.Builder()
            .addInterceptor(HttpLoggingInterceptor().apply {setLevel(HttpLoggingInterceptor.Level.BODY)})
            .build()
        val retrofit = Retrofit.Builder().baseUrl("http://10.0.2.2:8000/")
            .addConverterFactory(gsonConverterFactory)
            .client(client)
            .build()
        return retrofit.create(ApiService::class.java)
    }
}