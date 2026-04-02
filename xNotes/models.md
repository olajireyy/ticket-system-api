"""
        THE VIBECODER WAY:
        return Event.objects.all() 
        
        Why it fails: If you have 50 events, DRF will query the Event table 1 time. 
        Then, because our serializer asks for 'tickets', it will query the Ticket table 
        50 separate times (once for each event). 1 + 50 = 51 queries. 
        If you have 1000 events, that's 1001 queries. Your database will crash.
        """

        """
        THE ENGINEER WAY:
        We use prefetch_related(). This tells PostgreSQL: "Get all the events, 
        and while you're at it, get ALL the tickets for those events in ONE single query, 
        and stitch them together in memory."
        
        Result: 2 queries total, whether you have 5 events or 5,000.
        """



For Full Manual Control use APIView inetad of ListAPIView over the GET request