package com.example.smarthome.firebase

import android.util.Log
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage

class FirebaseNotificationService : FirebaseMessagingService() {
    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        remoteMessage.notification?.let {
            Log.d("FCM", "Notification: ${it.title} - ${it.body}")
        }
    }

    override fun onNewToken(token: String) {
        Log.d("FCM", "FCM Token: $token")
        // Store token to DB if needed
    }
} 