@router.get("/marketing")
def export_marketing(
    db: Session = Depends(get_db),
    venue_id: int = Query(None, description="ID площадки"),
    from_date: date = Query(None, description="Начало периода (YYYY-MM-DD)"),
    to_date: date = Query(None, description="Конец периода (YYYY-MM-DD)"),
    only_consented: bool = Query(False, description="Только с согласием на рекламу"),
    format: str = Query("csv", regex="^(csv|json)$"),
    current_user: User = Depends(get_current_venue_owner_or_admin)
):
    """
    Экспорт контактных данных для маркетинга.
    Доступно администратору и владельцу площадки.
    """
    venue_ids = get_venue_ids_for_user(current_user, db, venue_id)

    query = db.query(
        UserProfile.id,
        UserProfile.phone_number,
        UserProfile.email,
        UserProfile.full_name,
        UserProfile.marketing_consent,
        UserProfile.first_seen,
        UserProfile.venue_id
    ).filter(
        UserProfile.deleted_at.is_(None),
        UserProfile.venue_id.in_(venue_ids)
    )

    if only_consented:
        query = query.filter(UserProfile.marketing_consent == True)

    if from_date:
        query = query.filter(UserProfile.first_seen >= datetime.combine(from_date, datetime.min.time()))
    if to_date:
        query = query.filter(UserProfile.first_seen <= datetime.combine(to_date, datetime.max.time()))

    results = query.all()

    if format == "json":
        data = [{
            "id": r.id,
            "phone_number": r.phone_number,
            "email": r.email,
            "full_name": r.full_name,
            "marketing_consent": r.marketing_consent,
            "first_seen": r.first_seen.isoformat(),
            "venue_id": r.venue_id
        } for r in results]
        return JSONResponse(content=data)
    else:
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "phone_number", "email", "full_name", "marketing_consent", "first_seen", "venue_id"])
        for r in results:
            writer.writerow([
                r.id,
                r.phone_number or "",
                r.email or "",
                r.full_name or "",
                "1" if r.marketing_consent else "0",
                r.first_seen.isoformat(),
                r.venue_id
            ])
        output.seek(0)
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment;filename=marketing.csv"}
        )