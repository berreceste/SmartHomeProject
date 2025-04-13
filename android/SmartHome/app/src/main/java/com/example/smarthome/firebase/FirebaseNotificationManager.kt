package com.example.smarthome.firebase

import android.content.Context
import com.google.firebase.messaging.FirebaseMessaging
import kotlinx.coroutines.tasks.await

class FirebaseNotificationManager(private val context: Context) {

    suspend fun getToken(): String? {
        return try {
            FirebaseMessaging.getInstance().token.await()
        } catch (e: Exception) {
            null
        }
    }

    companion object {
        // You can use these methods to send notifications from your server
        // or from another part of your app
        const val FCM_SERVER_KEY = "YOUR_SERVER_KEY" // Replace with your Firebase Server Key
        
        // Example notification payload
        fun createNotificationPayload(
            title: String,
            body: String,
            token: String
        ): Map<String, String> {
            return mapOf(
                "to" to token,
                "notification" to """
                    {
                        "title": "$title",
                        "body": "$body"
                    }
                """.trimIndent()
            )
        }
    }
} 